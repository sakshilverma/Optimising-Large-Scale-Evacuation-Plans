graph [
  directed 1
  node [
    id 0
    label "A"
    weight 5
  ]
  node [
    id 1
    label "B"
    weight 10
  ]
  node [
    id 2
    label "O"
    weight 0
  ]
  edge [
    source 0
    target 1
    capacity 2
    length 1
  ]
  edge [
    source 0
    target 2
    capacity 4
    length 3
  ]
  edge [
    source 1
    target 2
    capacity 1
    length 2
  ]
  edge [
    source 1
    target 0
    capacity 1
    length 1
  ]
]
