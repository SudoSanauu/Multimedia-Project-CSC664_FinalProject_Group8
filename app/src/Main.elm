module Main exposing (Model, Msg(..), init, main, update, view)

import Array as A
import Browser
import Card as C exposing (Card)
import Data as D exposing (Data)
import Html exposing (Html, button, div, text)
import Html.Attributes exposing (class, style)
import Html.Events exposing (onClick)



-- MAIN


main =
    Browser.sandbox { init = init, update = update, view = view }



-- MODEL


type alias Model =
    { currentCard : Maybe Int }


init : Model
init =
    { currentCard = Nothing }



-- UPDATE


type Msg
    = SetCard Int
    | Reset


update : Msg -> Model -> Model
update msg model =
    case msg of
        SetCard n ->
            { model | currentCard = Just n }

        Reset ->
            { model | currentCard = Nothing }



-- VIEW


view : Model -> Html Msg
view model =
    let
        cardDisplay =
            case model.currentCard of
                Just n ->
                    displayRow n D.tempData

                Nothing ->
                    displayData D.tempData
    in
    div []
        [ text "My page wowee"
        , cardDisplay
        , button [ onClick Reset ] [ text "Reset" ]
        ]


displayRow : Int -> Data -> Html Msg
displayRow i data =
    let
        getCard index =
            case A.get index data.cardList of
                Just c ->
                    C.display c

                Nothing ->
                    error

        row =
            case A.get i data.cardRelationships of
                Just r ->
                    r

                Nothing ->
                    []

        mainCard =
            div [ class "mainCard" ]
                [ getCard i ]

        displayCardRel cardRel =
            div [ style "display" "inline-block", class "subCard" ]
                [ div [ style "display" "block", onClick (SetCard cardRel.cardIndex) ]
                    [ text <| String.fromFloat cardRel.distance, getCard cardRel.cardIndex ]
                ]
    in
    div [ class "cardRow" ]
        (mainCard :: List.map displayCardRel row)



-- Note, this function is a debug data dump, not made to look good


displayData : Data -> Html Msg
displayData data =
    div [] (List.map (\x -> displayRow x data) (List.range 0 data.numCards))


error : Html Msg
error =
    div [] [ text "ERROR" ]
