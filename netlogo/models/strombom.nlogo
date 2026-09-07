;; Strombom 2014 -- NetLogo twin of HerdSim algorithms/strombom
;;
;; Visual comparison: match HerdSim Single via Interface sliders, then setup / go.
;; HerdSim Single runs the Python reference of the same paper rules.
;;
;; Sheep: graze beyond r_s; else LCM attraction, neighbour/shepherd repulsion,
;;        inertia, and angular noise (Strombom eqs.).
;; Shepherd: Collect vs Drive using f(N) = r_a * N^(2/3); stop within 3*r_a.

breed [sheep a-sheep]
breed [herders herder]

sheep-own [
  prev-dx
  prev-dy
]

globals [
  arena-width
  arena-height
  goal-x
  goal-y
  mode-label
  run-status
  success-fraction
]

to setup
  clear-all
  ;; Slider/input values are kept after clear-all and reapplied to globals.
  ;; Defaults match HerdSim Strombom paper + drive_to_goal.
  random-seed sim-seed
  set arena-width 150
  set arena-height 150
  set goal-x 15
  set goal-y 15
  set mode-label "setup"
  set run-status "running"
  set success-fraction 1.0

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
    setxy (40 + random-float 50) (40 + random-float 50)
    set prev-dx 0
    set prev-dy 0
  ]

  create-herders initial-herders [
    set shape "default"
    set color yellow
    set size 4
    setxy (100 + random-float 30) (100 + random-float 30)
  ]

  reset-ticks
end

to-report clamp-x [x]
  report max (list 0 (min (list arena-width x)))
end

to-report clamp-y [y]
  report max (list 0 (min (list arena-height y)))
end

to-report unit-x [ux uy]
  let len sqrt (ux * ux + uy * uy)
  if len < 1e-9 [ report 0 ]
  report ux / len
end

to-report unit-y [ux uy]
  let len sqrt (ux * ux + uy * uy)
  if len < 1e-9 [ report 0 ]
  report uy / len
end

to-report random-noise-xy
  let angle random-float 360
  report (list (noise-strength * cos angle) (noise-strength * sin angle))
end

to-report sheep-gcm-x
  report mean [xcor] of sheep
end

to-report sheep-gcm-y
  report mean [ycor] of sheep
end

to-report collect-threshold
  report r-a * (count sheep ^ (2 / 3)) * collect-threshold-scale
end

to-report should-collect?
  if count sheep = 0 [ report false ]
  let gcx sheep-gcm-x
  let gcy sheep-gcm-y
  let farthest max-one-of sheep [ distancexy gcx gcy ]
  report [distancexy gcx gcy] of farthest > collect-threshold
end

to update-sheep
  if count sheep = 0 [ stop ]
  let herder-list sort herders

  ask sheep [
    let sx xcor
    let sy ycor
    let min-shep-dist 1e9
    foreach herder-list [ h ->
      let d distance h
      if d < min-shep-dist [ set min-shep-dist d ]
    ]

    ifelse min-shep-dist > r-s [
      ifelse random-float 1 < graze-move-prob [
        let nxy random-noise-xy
        let ux unit-x (item 0 nxy) (item 1 nxy)
        let uy unit-y (item 0 nxy) (item 1 nxy)
        setxy (clamp-x (sx + ux * sheep-speed)) (clamp-y (sy + uy * sheep-speed))
        set prev-dx ux * sheep-speed
        set prev-dy uy * sheep-speed
      ] [
        set prev-dx 0
        set prev-dy 0
      ]
    ] [
      let others sheep with [ self != myself ]
      let lcmx sx
      let lcmy sy
      if any? others [
        set lcmx mean [xcor] of others
        set lcmy mean [ycor] of others
      ]
      let ax lcmx - sx
      let ay lcmy - sy

      let rx 0
      let ry 0
      foreach sort others [ o ->
        let d distance o
        if d < r-a and d > 1e-9 [
          let ox sx - [xcor] of o
          let oy sy - [ycor] of o
          set rx rx + (ox / d)
          set ry ry + (oy / d)
        ]
      ]

      let hx 0
      let hy 0
      foreach herder-list [ h ->
        let d distance h
        if d < r-s and d > 1e-9 [
          let ox sx - [xcor] of h
          let oy sy - [ycor] of h
          set hx hx + (ox / d)
          set hy hy + (oy / d)
        ]
      ]

      let pdx prev-dx
      let pdy prev-dy
      let plen sqrt (pdx * pdx + pdy * pdy)
      if plen > 1e-9 [
        set pdx pdx / plen
        set pdy pdy / plen
      ]

      let nxy random-noise-xy
      let hxdg inertia * pdx + c-attr * ax + r-a * rx + hx + item 0 nxy
      let hydg inertia * pdy + c-attr * ay + r-a * ry + hy + item 1 nxy
      let ux unit-x hxdg hydg
      let uy unit-y hxdg hydg
      setxy (clamp-x (sx + ux * sheep-speed)) (clamp-y (sy + uy * sheep-speed))
      set prev-dx ux * sheep-speed
      set prev-dy uy * sheep-speed
    ]
  ]
end

to update-herders
  if count herders = 0 [ stop ]
  if count sheep = 0 [ stop ]

  let gcx sheep-gcm-x
  let gcy sheep-gcm-y
  let collecting? should-collect?
  ifelse collecting?
    [ set mode-label "collect" ]
    [ set mode-label "drive" ]

  let farthest max-one-of sheep [ distancexy gcx gcy ]
  let far-x [xcor] of farthest
  let far-y [ycor] of farthest

  let target-x gcx
  let target-y gcy
  ifelse collecting? [
    let behind-x far-x - gcx
    let behind-y far-y - gcy
    let blen sqrt (behind-x * behind-x + behind-y * behind-y)
    ifelse blen > 1e-9 [
      set target-x far-x + (behind-x / blen) * r-a
      set target-y far-y + (behind-y / blen) * r-a
    ] [
      set target-x far-x
      set target-y far-y
    ]
  ] [
    let drive-standoff r-a * sqrt (count sheep)
    let away-x gcx - goal-x
    let away-y gcy - goal-y
    let alen sqrt (away-x * away-x + away-y * away-y)
    ifelse alen > 1e-9 [
      set target-x gcx + (away-x / alen) * drive-standoff
      set target-y gcy + (away-y / alen) * drive-standoff
    ] [
      set target-x gcx
      set target-y gcy
    ]
  ]

  ask herders [
    let min-sheep-dist min [distance myself] of sheep
    if min-sheep-dist <= shepherd-stop-multiple * r-a [ stop ]

    let delta-x target-x - xcor
    let delta-y target-y - ycor
    let dist sqrt (delta-x * delta-x + delta-y * delta-y)
    if dist > 1e-9 [
      let step-len shepherd-speed
      let nxy random-noise-xy
      let mx (delta-x / dist) + item 0 nxy
      let my (delta-y / dist) + item 1 nxy
      let ux unit-x mx my
      let uy unit-y mx my
      setxy (clamp-x (xcor + ux * step-len)) (clamp-y (ycor + uy * step-len))
    ]
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
  update-herders
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
mode
mode-label
3
1
11

MONITOR
110
95
195
140
status
run-status
3
1
11

MONITOR
25
145
102
190
in goal
sheep-in-goal-count
0
1
11

MONITOR
110
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
50.0
1
1
NIL
HORIZONTAL

SLIDER
25
245
195
278
initial-herders
initial-herders
1
8
1.0
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
445
195
478
r-s
r-s
10
100
65.0
1
1
NIL
HORIZONTAL

SLIDER
25
485
195
518
sheep-speed
sheep-speed
0.1
3
1.0
0.1
1
NIL
HORIZONTAL

SLIDER
25
525
195
558
shepherd-speed
shepherd-speed
0.1
4
1.5
0.1
1
NIL
HORIZONTAL

SLIDER
25
565
195
598
noise-strength
noise-strength
0
1
0.3
0.05
1
NIL
HORIZONTAL

SLIDER
25
605
195
638
inertia
inertia
0
1
0.5
0.05
1
NIL
HORIZONTAL

SLIDER
25
645
195
678
c-attr
c-attr
0.5
2
1.05
0.05
1
NIL
HORIZONTAL

SLIDER
25
685
195
718
graze-move-prob
graze-move-prob
0
0.5
0.05
0.01
1
NIL
HORIZONTAL

SLIDER
25
725
195
758
shepherd-stop-multiple
shepherd-stop-multiple
1
6
3.0
0.5
1
NIL
HORIZONTAL

SLIDER
25
765
195
798
collect-threshold-scale
collect-threshold-scale
0.5
3
1.0
0.1
1
NIL
HORIZONTAL

TEXTBOX
25
810
210
880
Match HerdSim Single:\nsheep, shepherds, seed,\nmax_ticks, goal_radius,\nand Strombom paper params.\nAdjust sliders, then setup.
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
