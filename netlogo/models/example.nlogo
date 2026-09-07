;; HerdSim example NetLogo model (desktop demo)
;;
;; Open this file from the HerdSim NetLogo tab ("Open in NetLogo"), then click
;; setup and go in the NetLogo Interface. This is a normal NetLogo model --
;; HerdSim does not run it inside the browser canvas.
;;
;; Demo behavior:
;;   - Shepherds (herders) move toward the flock centroid
;;   - Sheep flee nearby herders and drift toward the goal

breed [sheep a-sheep]
breed [herders herder]

globals [
  sheep-x-list
  sheep-y-list
  shepherd-x-list
  shepherd-y-list
  arena-width
  arena-height
  dt
  goal-x
  goal-y
  goal-radius
  sheep-speed
  shepherd-speed
  flee-radius
  initial-sheep
  initial-herders
]

to setup
  clear-all
  set arena-width 150
  set arena-height 150
  set dt 0.1
  set goal-x 15
  set goal-y 15
  set goal-radius 15
  set sheep-speed 1.0
  set shepherd-speed 1.5
  set flee-radius 25
  set initial-sheep 30
  set initial-herders 1

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
    setxy (30 + random-float 40) (30 + random-float 40)
  ]

  create-herders initial-herders [
    set shape "default"
    set color yellow
    set size 4
    setxy 80 80
  ]

  sync-lists-from-turtles
  reset-ticks
end

to-report clamp-x [x]
  report max (list 0 (min (list arena-width x)))
end

to-report clamp-y [y]
  report max (list 0 (min (list arena-height y)))
end

to sync-lists-from-turtles
  set sheep-x-list []
  set sheep-y-list []
  foreach sort sheep [ t ->
    set sheep-x-list lput [xcor] of t sheep-x-list
    set sheep-y-list lput [ycor] of t sheep-y-list
  ]

  set shepherd-x-list []
  set shepherd-y-list []
  foreach sort herders [ t ->
    set shepherd-x-list lput [xcor] of t shepherd-x-list
    set shepherd-y-list lput [ycor] of t shepherd-y-list
  ]
end

to sync-turtles-from-lists
  let n length sheep-x-list
  let m length shepherd-x-list

  ;; Match sheep count to list length
  if count sheep < n [
    create-sheep (n - count sheep) [
      set shape "circle"
      set color white
      set size 2.5
    ]
  ]
  if count sheep > n [
    ask n-of (count sheep - n) sheep [ die ]
  ]

  if count herders < m [
    create-herders (m - count herders) [
      set shape "default"
      set color yellow
      set size 4
    ]
  ]
  if count herders > m [
    ask n-of (count herders - m) herders [ die ]
  ]

  let i 0
  foreach sort sheep [ t ->
    ask t [
      setxy (item i sheep-x-list) (item i sheep-y-list)
    ]
    set i i + 1
  ]

  set i 0
  foreach sort herders [ t ->
    ask t [
      setxy (item i shepherd-x-list) (item i shepherd-y-list)
    ]
    set i i + 1
  ]
end

to update-herders
  if count herders = 0 [ stop ]
  if count sheep = 0 [ stop ]

  let cx mean [xcor] of sheep
  let cy mean [ycor] of sheep

  ask herders [
    let delta-x cx - xcor
    let delta-y cy - ycor
    let dist sqrt (delta-x * delta-x + delta-y * delta-y)
    if dist > 1e-6 [
      let step-len shepherd-speed * dt
      setxy
        (clamp-x (xcor + (delta-x / dist) * step-len))
        (clamp-y (ycor + (delta-y / dist) * step-len))
    ]
  ]
end

to update-sheep-agents
  if count sheep = 0 [ stop ]

  ask sheep [
    let fx 0
    let fy 0
    let sx xcor
    let sy ycor

    foreach sort herders [ h ->
      let hx [xcor] of h
      let hy [ycor] of h
      let delta-x sx - hx
      let delta-y sy - hy
      let dist sqrt (delta-x * delta-x + delta-y * delta-y)
      if dist < flee-radius and dist > 1e-6 [
        let strength (flee-radius - dist) / flee-radius
        set fx fx + (delta-x / dist) * strength
        set fy fy + (delta-y / dist) * strength
      ]
    ]

    let goal-delta-x goal-x - sx
    let goal-delta-y goal-y - sy
    let gdist sqrt (goal-delta-x * goal-delta-x + goal-delta-y * goal-delta-y)
    if gdist > 1e-6 [
      set fx fx + 0.35 * (goal-delta-x / gdist)
      set fy fy + 0.35 * (goal-delta-y / gdist)
    ]

    let flen sqrt (fx * fx + fy * fy)
    if flen > 1e-6 [
      let step-len sheep-speed * dt
      setxy
        (clamp-x (sx + (fx / flen) * step-len))
        (clamp-y (sy + (fy / flen) * step-len))
    ]
  ]
end

to go
  ;; HerdSim fills lists before each go; desktop setup already filled them.
  if (length sheep-x-list > 0) or (length shepherd-x-list > 0) [
    sync-turtles-from-lists
  ]
  update-herders
  update-sheep-agents
  sync-lists-from-turtles
  tick
end
@#$#@#$#@
GRAPHICS-WINDOW
215
10
680
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
50
100
83
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
50
185
83
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

TEXTBOX
25
100
200
150
White circles = sheep\nYellow = shepherd\nGreen disc = goal\n\nClick setup, then go.
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
