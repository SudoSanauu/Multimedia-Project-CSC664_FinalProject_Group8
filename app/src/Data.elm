module Data exposing (CardRelationship, Data, RelationMatrix(..), createData, tempData, tempDist, tempNames)

import Array as A exposing (Array, get)
import Card as C exposing (Card)
import Html exposing (Html, div, text)
import Html.Attributes exposing (style)


type RelationMatrix
    = RelationMatrix (Array (Array Float))


type alias CardRelationship =
    { cardIndex : Int
    , distance : Float
    }


type alias Data =
    { numCards : Int
    , cardRelationships : Array (List CardRelationship)
    , cardList : Array Card
    }


createData : Array (Array Float) -> Array Card -> Data
createData distanceMatrix cardList =
    let
        ff j element =
            { cardIndex = j
            , distance = element
            }

        f row =
            List.sortBy .distance <| A.toList <| A.indexedMap ff row
    in
    { numCards = A.length cardList
    , cardRelationships =
        A.map f distanceMatrix
    , cardList = cardList
    }


tempData : Data
tempData =
    createData tempDist tempNames


tempDist : Array (Array Float)
tempDist =
    A.fromList <|
        List.map A.fromList
            [ [ 0.0, 7.5, 3.0, 5.0, 0.5, 6.0, 6.0, 7.75, 7.5, 0.5, 7.0, 6.0, 7.5, 8.5, 4.0, 7.5, 6.0 ]
            , [ 7.5, 0.0, 6.5, 6.5, 7.5, 4.5, 8.0, 3.0, 2.0, 7.5, 4.0, 8.5, 2.0, 8.5, 7.5, 1.0, 9.0 ]
            , [ 3.0, 6.5, 0.0, 2.0, 2.75, 7.5, 4.5, 6.0, 6.0, 2.75, 6.5, 5.5, 6.5, 7.0, 4.5, 6.5, 9.0 ]
            , [ 5.0, 6.5, 2.0, 0.0, 4.75, 7.5, 4.5, 6.0, 6.0, 4.75, 6.5, 5.5, 6.5, 7.0, 6.0, 6.5, 9.0 ]
            , [ 0.5, 7.5, 2.75, 4.75, 0.0, 6.0, 6.0, 7.75, 7.5, 0.5, 7.0, 5.75, 7.5, 8.5, 4.0, 7.5, 6.0 ]
            , [ 6.0, 4.5, 7.5, 7.5, 6.0, 0.0, 9.0, 5.5, 4.0, 6.0, 6.0, 9.0, 4.0, 9.0, 4.0, 4.0, 3.75 ]
            , [ 6.0, 8.0, 4.5, 4.5, 6.0, 9.0, 0.0, 7.5, 7.0, 6.0, 8.0, 6.0, 9.0, 4.0, 8.0, 8.0, 9.0 ]
            , [ 7.75, 3.0, 6.0, 6.0, 7.75, 5.5, 7.5, 0.0, 1.5, 7.75, 3.0, 9.0, 3.0, 8.5, 8.0, 2.5, 8.0 ]
            , [ 7.5, 2.0, 6.0, 6.0, 7.5, 4.0, 7.0, 1.5, 0.0, 7.5, 3.5, 9.0, 2.0, 9.0, 7.0, 1.5, 6.0 ]
            , [ 0.5, 7.5, 2.75, 4.75, 0.5, 6.0, 6.0, 7.75, 7.5, 0.0, 7.0, 5.75, 7.5, 8.5, 4.0, 7.5, 6.0 ]
            , [ 7.0, 4.0, 6.5, 6.5, 7.0, 6.0, 8.0, 3.0, 3.5, 7.0, 0.0, 6.0, 2.5, 6.0, 7.5, 3.75, 8.0 ]
            , [ 6.0, 8.5, 5.5, 5.5, 5.75, 9.0, 6.0, 9.0, 9.0, 5.75, 6.0, 0.0, 5.75, 5.5, 7.5, 9.0, 8.5 ]
            , [ 7.5, 2.0, 6.5, 6.5, 7.5, 4.0, 9.0, 3.0, 2.0, 7.5, 2.5, 5.75, 0.0, 6.0, 7.0, 1.75, 8.0 ]
            , [ 8.5, 8.5, 7.0, 7.0, 8.5, 9.0, 4.0, 8.5, 9.0, 8.5, 6.0, 5.5, 6.0, 0.0, 9.0, 9.0, 8.5 ]
            , [ 4.0, 7.5, 4.5, 6.0, 4.0, 4.0, 8.0, 8.0, 7.0, 4.0, 7.5, 7.5, 7.0, 9.0, 0.0, 8.75, 6.5 ]
            , [ 7.5, 1.0, 6.5, 6.5, 7.5, 4.0, 8.0, 2.5, 1.5, 7.5, 3.75, 9.0, 1.75, 9.0, 8.75, 0.0, 7.0 ]
            , [ 6.0, 9.0, 9.0, 9.0, 6.0, 3.75, 9.0, 8.0, 6.0, 6.0, 8.0, 8.5, 8.0, 8.5, 6.5, 7.0, 0.0 ]
            ]


tempNames : Array Card
tempNames =
    A.fromList
        [ { name = "Aether Adept"
          , imgUrl = "https://img.scryfall.com/cards/large/front/1/6/1640b76d-15d6-4b08-a34b-c5432259d570.jpg?1562900340"
          }
        , { name = "Agonizing Syphon"
          , imgUrl = "https://img.scryfall.com/cards/large/front/0/d/0d8efd95-1c2f-4dd1-b70b-3cfb10ff3a28.jpg?1563898795"
          }
        , { name = "Arrester's Admonition"
          , imgUrl = "https://img.scryfall.com/cards/large/front/6/3/637c2d6a-e6b8-4dc5-81aa-da1b7384e006.jpg?1584830115"
          }
        , { name = "Code of Constraint"
          , imgUrl = "https://img.scryfall.com/cards/large/front/2/5/258aeef1-565a-4f19-b12c-d46d54ba231d.jpg?1584830168"
          }
        , { name = "Exclusion Mage"
          , imgUrl = "https://img.scryfall.com/cards/large/front/c/c/ccad82f5-5c5c-42ad-b66e-942f0d9631ca.jpg?1562304356"
          }
        , { name = "Firemane Avenger"
          , imgUrl = "https://img.scryfall.com/cards/large/front/e/2/e244c198-efdc-492a-9c52-76aac006de9d.jpg?1561849759"
          }
        , { name = "Impulse"
          , imgUrl = "https://img.scryfall.com/cards/large/front/b/d/bda887f9-ea83-435e-b9d6-48f979a5fdb7.jpg?1573507735"
          }
        , { name = "Lightning Bolt"
          , imgUrl = "https://img.scryfall.com/cards/large/front/3/2/32a180dd-9641-4546-8940-9b21084f0c71.jpg?1573512170"
          }
        , { name = "Lightning Helix"
          , imgUrl = "https://img.scryfall.com/cards/large/front/3/e/3e897af5-d450-4a7c-a02a-543914c2c680.jpg?1573515403"
          }
        , { name = "Man-o'-War"
          , imgUrl = "https://img.scryfall.com/cards/large/front/0/a/0a767474-ba5a-4141-a926-a384bb1d3626.jpg?1573507864"
          }
        , { name = "Oath of Chandra"
          , imgUrl = "https://img.scryfall.com/cards/large/front/f/5/f570b0cb-2f38-422d-89d6-22c85e085328.jpg?1562944439"
          }
        , { name = "Oath of Jace"
          , imgUrl = "https://img.scryfall.com/cards/large/front/e/8/e8e7b007-a14b-40b2-9de7-38545c50a073.jpg?1562941723"
          }
        , { name = "Oath of Kaya"
          , imgUrl = "https://img.scryfall.com/cards/large/front/f/a/faba010d-5b1b-4562-91d6-ec55303c4dcd.jpg?1559959445"
          }
        , { name = "Oath of Nissa"
          , imgUrl = "https://img.scryfall.com/cards/large/front/6/1/613513ea-55dd-4ae8-93b2-247e468112a6.jpg?1574294106"
          }
        , { name = "Skymark Roc"
          , imgUrl = "https://img.scryfall.com/cards/large/front/6/0/60601296-2229-4c48-94cc-1903926750ce.jpg?1562787112"
          }
        , { name = "Smiting Helix"
          , imgUrl = "https://img.scryfall.com/cards/large/front/0/7/07c17401-6b4d-4280-8962-46e380ab2bf4.jpg?1573510530"
          }
        , { name = "Tajic, Blade of the Legion"
          , imgUrl = "https://img.scryfall.com/cards/large/front/b/e/be5717c1-338e-446c-aa7e-93e79e4abb72.jpg?1562930543"
          }
        ]
