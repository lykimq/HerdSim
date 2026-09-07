;; Strombom Noise -- NetLogo twin of HerdSim algorithms/strombom_noise
;;
;; Same Collect/Drive as Strombom 2014 with elevated sheep noise and lower inertia
;; (HerdSim defaults: noise_strength=0.9, inertia=0.35).
;; Match HerdSim Single via Interface sliders, then setup / go.

breed [sheep a-sheep]
breed [herders herder]

herders-own [
  path-x
  path-y
]

sheep-own [
  prev-dx
  prev-dy
]

globals [
  time-to-goal
  herder-path-length
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
  ;; Defaults match HerdSim Strombom Noise + drive_to_goal.
  random-seed sim-seed
  ;; Spawn matches HerdSim drive_to_goal (center +/- 30; herders near 125 +/- 5).
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
    setxy (75 - 30 + random-float 60) (75 - 30 + random-float 60)
    set prev-dx 0
    set prev-dy 0
  ]

  create-herders initial-herders [
    set shape "default"
    set color yellow
    set size 4
    setxy (125 - 5 + random-float 10) (125 - 5 + random-float 10)
  ]


  set herder-path-length 0
  set time-to-goal -1
  
  clear-output
  ask herders [
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
        setxy (reflect-x (sx + ux * sheep-speed)) (reflect-y (sy + uy * sheep-speed))
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
        ifelse (n-neighbors < 0) or (n-neighbors >= count others) [
          set lcmx mean [xcor] of others
          set lcmy mean [ycor] of others
        ] [
          let nearest min-n-of n-neighbors others [ distance myself ]
          set lcmx mean [xcor] of nearest
          set lcmy mean [ycor] of nearest
        ]
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
      let hxdg inertia * pdx + c-attr * ax + r-a * rx + rs-weight * hx + item 0 nxy
      let hydg inertia * pdy + c-attr * ay + r-a * ry + rs-weight * hy + item 1 nxy
      let ux unit-x hxdg hydg
      let uy unit-y hxdg hydg
      setxy (reflect-x (sx + ux * sheep-speed)) (reflect-y (sy + uy * sheep-speed))
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
      setxy (reflect-x (xcor + ux * step-len)) (reflect-y (ycor + uy * step-len))
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


; === comparison metrics (HerdSim-aligned) ===

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
  let movers sheep with [ (prev-dx * prev-dx + prev-dy * prev-dy) > 1e-20 ]
  if not any? movers [ report 0 ]
  let mx mean [ prev-dx / sqrt (prev-dx * prev-dx + prev-dy * prev-dy) ] of movers
  let my mean [ prev-dy / sqrt (prev-dx * prev-dx + prev-dy * prev-dy) ] of movers
  report sqrt (mx * mx + my * my)
end

to apply-trails
  ifelse show-trails [
    ask herders [
      set pen-size 2
      pen-down
    ]
  ] [
    ask herders [ pen-up ]
  ]
end

to update-herder-path
  ask herders [
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
  let spd sqrt (prev-dx * prev-dx + prev-dy * prev-dy)
  if spd <= 1e-9 [ report heading ]
  report atan prev-dx prev-dy
end

to clear-trails
  clear-drawing
  apply-trails
end

to toggle-follow-herder
  ifelse subject = nobody [
    if any? herders [ follow one-of herders ]
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
  update-herders
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
0.9
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
0.35
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

SLIDER
25
810
195
843
n-neighbors
n-neighbors
-1
50
-1.0
1
1
NIL
HORIZONTAL

SLIDER
25
855
195
888
rs-weight
rs-weight
0
3
1.0
0.1
1
NIL
HORIZONTAL

TEXTBOX
25
908
880
308
Match HerdSim Strombom Noise:\nsame Collect/Drive params;\ndefault noise 0.9, inertia 0.35.\nAdjust sliders, then setup.
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
(word count sheep " / " count herders)
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
