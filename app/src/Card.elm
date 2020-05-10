module Card exposing (Card, display, sampleCard)

import Html exposing (Html, div, img, text)
import Html.Attributes exposing (alt, src, style, width)
import String as S


type alias Card =
    { name : String
    , imgUrl : String
    }


sampleCard : Card
sampleCard =
    { name = "Island"
    , imgUrl = "https://img.scryfall.com/cards/large/front/9/0/90a57c0e-fa61-45ef-955d-d296403967d5.jpg?1559591389"
    }


display : Card -> Html msg
display c =
    div []
        [ div [] [ text (S.concat [ "Name: ", c.name ]) ]
        , img
            [ width 200
            , src c.imgUrl
            , alt c.name
            ]
            []
        ]
