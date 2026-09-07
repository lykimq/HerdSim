;; Kubo 2022 -- NetLogo twin of HerdSim algorithms/kubo
;;
;; Multi-dog repulsive-force herding (Kubo et al., 2022 / MATLAB port).
;; Match HerdSim Single via Interface sliders, then setup / go.
;; Compare with HerdSim Single -> Kubo 2022.
;;
;; Sheep forces: repulsion (a), alignment (b), cohesion (c), dog repulsion (d).
;; Dog forces: attract farthest-from-goal sheep (A), repel that sheep (B),
;;             repel goal (C), dog-dog repulsion (D).
;; Order: update sheep first, then dogs (MATLAB / HerdSim order).

breed [sheep a-sheep]
breed [dogs a-dog]

sheep-own [ vx vy ]
dogs-own [ vx vy ]

globals [
  arena-width
  arena-height
  goal-x
  goal-y
  eps
  run-status
  success-fraction
]

to setup
  clear-all
  ;; Slider values persist after clear-all (HerdSim-comparable settings).
  random-seed sim-seed
  set arena-width 150
  set arena-height 150
  set goal-x 15
  set goal-y 15
  set eps 1e-6
  set success-fraction 1.0
  set run-status "running"

  resize-world 0 arena-width 0 arena-height
  set-patch-size 3

  ask patches [
    ifelse distancexy goal-x goal-y <= goal-radius
      [ set pcolor green - 3 ]
      [ set pcolor 2 ]
  ]

  create-sheep initial-sheep [
    set shape "circle"
    set color white
    set size 2.5
    setxy (50 + random-float 40) (50 + random-float 40)
    set vx 0
    set vy 0
  ]

  create-dogs initial-dogs [
    set shape "default"
    set color orange
    set size 3.5
    setxy (110 + random-float 25) (110 + random-float 25)
    set vx 0
    set vy 0
  ]

  reset-ticks
end

to-report clamp-x [x]
  report max (list 0 (min (list arena-width x)))
end

to-report clamp-y [y]
  report max (list 0 (min (list arena-height y)))
end

to-report clamped-vel [sx sy max-speed]
  let spd sqrt (sx * sx + sy * sy)
  if spd <= max-speed or spd < eps [
    report (list sx sy)
  ]
  report (list (sx / spd * max-speed) (sy / spd * max-speed))
end

to update-sheep
  if count sheep = 0 [ stop ]
  let sheep-list sort sheep
  let dog-list sort dogs

  ;; Snapshot old velocities for alignment (use values before this tick)
  ask sheep [
    let px xcor
    let py ycor
    let force-ax 0
    let force-ay 0
    let force-bx 0
    let force-by 0
    let force-cx 0
    let force-cy 0
    let force-dx 0
    let force-dy 0
    let n-s 0
    let n-align 0

    foreach sheep-list [ other-sheep ->
      if other-sheep != self [
        let ox [xcor] of other-sheep
        let oy [ycor] of other-sheep
        let dist sqrt ((px - ox) * (px - ox) + (py - oy) * (py - oy))
        if dist < sense-radius and dist > 0 [
          set n-s n-s + 1
          let dsafe max (list dist eps)
          let rx px - ox
          let ry py - oy
          set force-ax force-ax + rx / (dsafe * dsafe)
          set force-ay force-ay + ry / (dsafe * dsafe)
          set force-cx force-cx - rx / dsafe
          set force-cy force-cy - ry / dsafe
          let ovx [vx] of other-sheep
          let ovy [vy] of other-sheep
          let ospd sqrt (ovx * ovx + ovy * ovy)
          if ospd > 0 [
            set force-bx force-bx + ovx / ospd
            set force-by force-by + ovy / ospd
            set n-align n-align + 1
          ]
        ]
      ]
    ]

    if n-s > 0 [
      set force-ax force-ax / n-s
      set force-ay force-ay / n-s
      set force-cx force-cx / n-s
      set force-cy force-cy / n-s
    ]
    if n-align > 0 [
      set force-bx force-bx / n-align
      set force-by force-by / n-align
    ]

    let n-d 0
    foreach dog-list [ d ->
      let ox [xcor] of d
      let oy [ycor] of d
      let dist sqrt ((px - ox) * (px - ox) + (py - oy) * (py - oy))
      if dist < sense-radius [
        set n-d n-d + 1
        let dsafe max (list dist eps)
        let rx px - ox
        let ry py - oy
        set force-dx force-dx + rx / (dsafe * dsafe * dsafe)
        set force-dy force-dy + ry / (dsafe * dsafe * dsafe)
      ]
    ]
    if n-d > 0 [
      set force-dx force-dx / n-d
      set force-dy force-dy / n-d
    ]

    let nvx k-s1 * force-ax + k-s2 * force-bx + k-s3 * force-cx + k-s4 * force-dx
    let nvy k-s1 * force-ay + k-s2 * force-by + k-s3 * force-cy + k-s4 * force-dy
    let clipped clamped-vel nvx nvy sheep-speed-max
    set vx item 0 clipped
    set vy item 1 clipped
  ]

  ask sheep [
    setxy (clamp-x (xcor + step-dt * vx)) (clamp-y (ycor + step-dt * vy))
  ]
end

to update-dogs
  if count dogs = 0 [ stop ]
  let dog-list sort dogs
  let sheep-list sort sheep

  ask dogs [
    let px xcor
    let py ycor
    let force-ax 0
    let force-ay 0
    let force-bx 0
    let force-by 0
    let force-cx 0
    let force-cy 0
    let force-dx 0
    let force-dy 0

    ;; Sheep in range
    let near-sheep []
    foreach sheep-list [ s ->
      let ox [xcor] of s
      let oy [ycor] of s
      let dist sqrt ((px - ox) * (px - ox) + (py - oy) * (py - oy))
      if dist < sense-radius [
        set near-sheep lput s near-sheep
      ]
    ]

    ifelse empty? near-sheep [
      let gx goal-x - px
      let gy goal-y - py
      let gdist sqrt (gx * gx + gy * gy)
      set force-cx 0.1 * gx / (gdist + eps)
      set force-cy 0.1 * gy / (gdist + eps)
    ] [
      ;; Target = sheep farthest from goal among those in range
      let target first near-sheep
      let best-d -1
      foreach near-sheep [ s ->
        let dgoal sqrt (([xcor] of s - goal-x) * ([xcor] of s - goal-x) + ([ycor] of s - goal-y) * ([ycor] of s - goal-y))
        if dgoal > best-d [
          set best-d dgoal
          set target s
        ]
      ]
      let tx [xcor] of target
      let ty [ycor] of target
      let diff-x px - tx
      let diff-y py - ty
      let dist sqrt (diff-x * diff-x + diff-y * diff-y)
      set force-ax 0 - diff-x / (dist + eps)
      set force-ay 0 - diff-y / (dist + eps)
      set force-bx diff-x / ((dist + eps) ^ 3)
      set force-by diff-y / ((dist + eps) ^ 3)

      let gx px - goal-x
      let gy py - goal-y
      let gdist sqrt (gx * gx + gy * gy)
      set force-cx gx / (gdist + eps)
      set force-cy gy / (gdist + eps)
    ]

    let n-dogs 0
    foreach dog-list [ other-dog ->
      if other-dog != self [
        let ox [xcor] of other-dog
        let oy [ycor] of other-dog
        let dist sqrt ((px - ox) * (px - ox) + (py - oy) * (py - oy))
        if dist < sense-radius and dist > 0 [
          set n-dogs n-dogs + 1
          let dsafe max (list dist eps)
          let rx px - ox
          let ry py - oy
          set force-dx force-dx + rx / (dsafe * dsafe * dsafe)
          set force-dy force-dy + ry / (dsafe * dsafe * dsafe)
        ]
      ]
    ]
    if n-dogs > 0 [
      set force-dx force-dx / n-dogs
      set force-dy force-dy / n-dogs
    ]

    let nvx k-f1 * force-ax + k-f2 * force-bx + k-f3 * force-cx + k-f4 * force-dx
    let nvy k-f1 * force-ay + k-f2 * force-by + k-f3 * force-cy + k-f4 * force-dy
    let clipped clamped-vel nvx nvy dog-speed-max
    set vx item 0 clipped
    set vy item 1 clipped
  ]

  ask dogs [
    setxy (clamp-x (xcor + step-dt * vx)) (clamp-y (ycor + step-dt * vy))
  ]
end

to-report sheep-in-goal-count
  report count sheep with [ distancexy goal-x goal-y <= goal-radius ]
end

to-report success?
  if count sheep = 0 [ report false ]
  report (sheep-in-goal-count / count sheep) >= success-fraction
end

to go
  if ticks >= max-ticks [
    set run-status "timeout"
    stop
  ]
  if success? [
    set run-status "success"
    stop
  ]
  update-sheep
  update-dogs
  tick
  if success? [
    set run-status "success"
    stop
  ]
  if ticks >= max-ticks [
    set run-status "timeout"
    stop
  ]
end
@#$#@#$#@
GRAPHICS-WINDOW
220
10
685
475
-1
-1
3.0
1
10
1
1
1
0
0
0
1
0
150
0
150
1
1
1
ticks
30.0

BUTTON
25
45
100
78
NIL
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
110
45
185
78
NIL
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
0

MONITOR
25
95
102
140
status
run-status
3
1
11

MONITOR
110
95
195
140
in goal
sheep-in-goal-count
0
1
11

MONITOR
25
145
195
190
ticks
(word ticks "/" max-ticks)
3
1
11

SLIDER
25
205
195
238
initial-sheep
initial-sheep
5
150
40.0
1
1
NIL
HORIZONTAL

SLIDER
25
245
195
278
initial-dogs
initial-dogs
1
8
4.0
1
1
NIL
HORIZONTAL

SLIDER
25
285
195
318
sim-seed
sim-seed
0
9999
42.0
1
1
NIL
HORIZONTAL

SLIDER
25
325
195
358
max-ticks
max-ticks
100
6000
3000.0
100
1
NIL
HORIZONTAL

SLIDER
25
365
195
398
goal-radius
goal-radius
5
40
15.0
1
1
NIL
HORIZONTAL

SLIDER
25
405
195
438
sense-radius
sense-radius
10
100
60.0
1
1
NIL
HORIZONTAL

SLIDER
25
445
195
478
step-dt
step-dt
0.01
0.2
0.05
0.01
1
NIL
HORIZONTAL

SLIDER
25
485
195
518
sheep-speed-max
sheep-speed-max
1
15
5.0
0.5
1
NIL
HORIZONTAL

SLIDER
25
525
195
558
dog-speed-max
dog-speed-max
1
20
10.0
0.5
1
NIL
HORIZONTAL

SLIDER
25
565
195
598
k-s1
k-s1
0
50
10.0
0.5
1
NIL
HORIZONTAL

SLIDER
25
605
195
638
k-s2
k-s2
0
5
0.5
0.1
1
NIL
HORIZONTAL

SLIDER
25
645
195
678
k-s3
k-s3
0
10
2.0
0.1
1
NIL
HORIZONTAL

SLIDER
25
685
195
718
k-s4
k-s4
0
10000
5000.0
100
1
NIL
HORIZONTAL

SLIDER
25
725
195
758
k-f1
k-f1
0
50
10.0
0.5
1
NIL
HORIZONTAL

SLIDER
25
765
195
798
k-f2
k-f2
0
1000
200.0
10
1
NIL
HORIZONTAL

SLIDER
25
805
195
838
k-f3
k-f3
0
50
8.0
0.5
1
NIL
HORIZONTAL

SLIDER
25
845
195
878
k-f4
k-f4
0
10000
3000.0
100
1
NIL
HORIZONTAL

TEXTBOX
25
890
210
960
Match HerdSim Single:\nsheep, dogs, seed,\nmax_ticks, goal_radius,\nradius/dt/speeds, and\nK_s*/K_f* gains.\nAdjust sliders, then setup.
11
0.0
1

@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
NetLogo 6.4.0
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
