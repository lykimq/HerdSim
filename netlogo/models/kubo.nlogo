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
dogs-own [
  path-x
  path-y vx vy ]

globals [
  mode-label
  time-to-goal
  herder-path-length
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
  ;; Spawn matches HerdSim drive_to_goal (center +/- 30; herders near 125 +/- 5).
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
    setxy (75 - 30 + random-float 60) (75 - 30 + random-float 60)
    set vx 0
    set vy 0
  ]

  create-dogs initial-dogs [
    set shape "default"
    set color orange
    set size 3.5
    setxy (125 - 5 + random-float 10) (125 - 5 + random-float 10)
    set vx 0
    set vy 0
  ]


  set herder-path-length 0
  set time-to-goal -1
  set mode-label "force"
  clear-output
  ask dogs [
    set path-x xcor
    set path-y ycor
  ]
  apply-trails

  reset-ticks
end

;; Match HerdSim World.reflect_positions (elastic bounce, one pass).
to-report reflect-x [x]
  let px x
  if px < 0 [ set px 0 - px ]
  if px > arena-width [ set px (2 * arena-width) - px ]
  report max (list 0 (min (list arena-width px)))
end

to-report reflect-y [y]
  let py y
  if py < 0 [ set py 0 - py ]
  if py > arena-height [ set py (2 * arena-height) - py ]
  report max (list 0 (min (list arena-height py)))
end

to-report clamped-vel [sx sy max-speed]
  let spd sqrt (sx * sx + sy * sy)
  if spd <= max-speed or spd < eps [
    report (list sx sy)
  ]
  report (list (sx / spd * max-speed) (sy / spd * max-speed))
end

;; Match HerdSim reflect_positions + reflect_velocities for force agents.
to step-with-reflect
  let nx xcor + step-dt * vx
  let ny ycor + step-dt * vy
  let hit-x false
  let hit-y false
  if nx < 0 [
    set nx 0 - nx
    set hit-x true
  ]
  if nx > arena-width [
    set nx (2 * arena-width) - nx
    set hit-x true
  ]
  if ny < 0 [
    set ny 0 - ny
    set hit-y true
  ]
  if ny > arena-height [
    set ny (2 * arena-height) - ny
    set hit-y true
  ]
  setxy (max (list 0 (min (list arena-width nx)))) (max (list 0 (min (list arena-height ny))))
  if hit-x [ set vx 0 - vx ]
  if hit-y [ set vy 0 - vy ]
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
    step-with-reflect
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
    step-with-reflect
  ]
end

to-report sheep-in-goal-count
  report count sheep with [ distancexy goal-x goal-y <= goal-radius ]
end

to-report success?
  if count sheep = 0 [ report false ]
  report (sheep-in-goal-count / count sheep) >= success-fraction
end


; === comparison metrics (HerdSim-aligned) ===

to-report collect-threshold
  report r-a * (count sheep ^ (2 / 3))
end

to-report sheep-in-goal-frac
  if count sheep = 0 [ report 0 ]
  report sheep-in-goal-count / count sheep
end

to-report flock-cohesion
  if count sheep = 0 [ report 0 ]
  let gcx mean [xcor] of sheep
  let gcy mean [ycor] of sheep
  report mean [ distancexy gcx gcy ] of sheep
end

to-report outlier-count
  if count sheep = 0 [ report 0 ]
  let gcx mean [xcor] of sheep
  let gcy mean [ycor] of sheep
  let thresh collect-threshold
  report count sheep with [ distancexy gcx gcy > thresh ]
end

to-report gcm-to-goal
  if count sheep = 0 [ report 0 ]
  let gcx mean [xcor] of sheep
  let gcy mean [ycor] of sheep
  report sqrt ((gcx - goal-x) * (gcx - goal-x) + (gcy - goal-y) * (gcy - goal-y))
end

to-report flock-polarization
  if count sheep = 0 [ report 0 ]
  let movers sheep with [ (vx * vx + vy * vy) > 1e-20 ]
  if not any? movers [ report 0 ]
  let mx mean [ vx / sqrt (vx * vx + vy * vy) ] of movers
  let my mean [ vy / sqrt (vx * vx + vy * vy) ] of movers
  report sqrt (mx * mx + my * my)
end

to apply-trails
  ifelse show-trails [
    ask dogs [
      set pen-size 2
      pen-down
    ]
  ] [
    ask dogs [ pen-up ]
  ]
end

to update-herder-path
  ask dogs [
    set herder-path-length herder-path-length + distancexy path-x path-y
    set path-x xcor
    set path-y ycor
  ]
end

to update-comparison-metrics
  update-herder-path
  if (time-to-goal < 0) and success? [
    set time-to-goal ticks
  ]
  apply-trails
end

to write-run-summary
  clear-output
  output-print "metric,value"
  output-print (word "status," run-status)
  output-print (word "ticks," ticks)
  output-print (word "time_to_goal," time-to-goal)
  output-print (word "sheep_in_goal," sheep-in-goal-count)
  output-print (word "sheep_in_goal_frac," precision sheep-in-goal-frac 4)
  output-print (word "cohesion," precision flock-cohesion 3)
  output-print (word "min_separation," precision min-separation 3)
  output-print (word "outlier_count," outlier-count)
  output-print (word "gcm_goal_dist," precision gcm-to-goal 3)
  output-print (word "polarization," precision flock-polarization 4)
  output-print (word "shepherd_path," precision herder-path-length 3)
  output-print (word "mode," mode-label)
  output-print (word "seed," sim-seed)
end

to finish-run [ status-name ]
  set run-status status-name
  if (status-name = "success") and (time-to-goal < 0) [
    set time-to-goal ticks
  ]
  write-run-summary
end


; === research panel helpers ===
to-report min-separation
  if count sheep < 2 [ report 0 ]
  let best 1e9
  let alist sort sheep
  let n length alist
  let i 0
  while [i < (n - 1)] [
    let a item i alist
    let j i + 1
    while [j < n] [
      let d [distance (item j alist)] of a
      if d < best [ set best d ]
      set j j + 1
    ]
    set i i + 1
  ]
  report best
end

to-report sheep-heading-deg
  ;; Degrees from velocity components (NetLogo atan is atan2(dx, dy) style: atan dx dy).
  let spd sqrt (vx * vx + vy * vy)
  if spd <= 1e-9 [ report heading ]
  report atan vx vy
end

to clear-trails
  clear-drawing
  apply-trails
end

to toggle-follow-herder
  ifelse subject = nobody [
    if any? dogs [ follow one-of dogs ]
  ] [
    reset-perspective
  ]
end

to go
  if ticks >= max-ticks [
    finish-run "timeout"
    stop
  ]
  if success? [
    finish-run "success"
    stop
  ]
  update-sheep
  update-dogs
  tick
  update-comparison-metrics
  if success? [
    finish-run "success"
    stop
  ]
  if ticks >= max-ticks [
    finish-run "timeout"
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
410
195
443
r-a
r-a
0.5
10
2.0
0.5
1
NIL
HORIZONTAL

SLIDER
25
450
195
483
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
490
195
523
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
530
195
563
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
570
195
603
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
610
195
643
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
650
195
683
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
690
195
723
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
730
195
763
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
770
195
803
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
810
195
843
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
850
195
883
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
890
195
923
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
935
210
1005
Match HerdSim Single:\nsheep, dogs, seed,\nmax_ticks, goal_radius,\nradius/dt/speeds, and\nK_s*/K_f* gains.\nAdjust sliders, then setup.
11
0.0
1

BUTTON
700
10
980
43
go once
go
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1


SWITCH
700
55
860
88
show-trails
show-trails
0
1
-1000

MONITOR
700
100
840
145
in goal %
precision sheep-in-goal-frac 3
3
1
11

MONITOR
850
100
980
145
cohesion
precision flock-cohesion 2
3
1
11

MONITOR
700
155
840
200
outliers
outlier-count
0
1
11

MONITOR
850
155
980
200
GCM-goal
precision gcm-to-goal 2
3
1
11

MONITOR
700
210
840
255
polarisation
precision flock-polarization 3
3
1
11

MONITOR
850
210
980
255
herder path
precision herder-path-length 1
3
1
11

MONITOR
700
265
840
310
time to goal
time-to-goal
0
1
11

MONITOR
850
265
980
310
sheep / dogs
(word count sheep " / " count dogs)
3
1
11

PLOT
700
320
980
470
Sheep in goal
tick
sheep
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"in-goal" 1.0 0 -16777216 true "" "plot sheep-in-goal-count"

PLOT
700
480
980
630
Flock cohesion
tick
mean dist
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"cohesion" 1.0 0 -2674135 true "" "plot flock-cohesion"

PLOT
700
640
980
790
GCM to goal
tick
distance
0.0
10.0
0.0
10.0
true
false
"" ""
PENS
"gcm-goal" 1.0 0 -13345367 true "" "plot gcm-to-goal"

OUTPUT
700
800
980
920
11

TEXTBOX
700
930
980
990
Comparison panel: metrics, trails, plots;\nresearch panel (right) adds histograms\nand camera / trail tools.
11
0.0
1

BUTTON
1000
10
1140
43
follow herder
toggle-follow-herder
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
1150
10
1290
43
clear trails
clear-trails
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

MONITOR
1000
55
1140
100
min sep
precision min-separation 2
3
1
11

PLOT
1000
110
1290
280
Heading histogram
heading
count
0.0
360.0
0.0
10.0
true
false
"" ""
PENS
"headings" 1.0 1 -16777216 true "" "histogram [sheep-heading-deg] of sheep"

PLOT
1000
290
1290
460
GCM distance histogram
dist to GCM
count
0.0
50.0
0.0
10.0
true
false
"" ""
PENS
"gcm-dist" 1.0 1 -13345367 true "" "if any? sheep [ let gcx mean [xcor] of sheep let gcy mean [ycor] of sheep histogram [ distancexy gcx gcy ] of sheep ]"

TEXTBOX
1000
470
1290
530
Research panel: histograms, min separation,\nfollow camera, clear trails. Observations\nfeed future HerdSim feature ideas.
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
