module Main exposing (Model, Msg(..), init, main, update, view)

--import Debug exposing (log, toString)

import Array as A exposing (Array)
import Browser
import Card as C exposing (Card)
import Data as D exposing (Data)
import File exposing (File)
import File.Select exposing (file)
import Html exposing (Html, a, button, div, text)
import Html.Attributes exposing (class, href, style)
import Html.Events exposing (onClick)
import Json.Decode as Decode exposing (Decoder, decodeString, field)
import Task



-- MAIN


main =
    Browser.element
        { init = init
        , update = update
        , view = view
        , subscriptions = subscriptions
        }



-- MODEL


type Model
    = Empty
    | ShowCards { currentCard : Maybe Int, data : Data }
    | Broken String


init : () -> ( Model, Cmd Msg )
init _ =
    ( Empty, Cmd.none )



-- UPDATE


type Msg
    = SetCard Int
    | Reset
    | RequestData
    | DataLoaded File
    | DecodeFile String


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case ( msg, model ) of
        ( SetCard n, ShowCards mod ) ->
            ( ShowCards { mod | currentCard = Just n }, Cmd.none )

        ( Reset, _ ) ->
            ( Empty, Cmd.none )

        ( RequestData, Empty ) ->
            ( model, requestJson )

        ( DataLoaded f, Empty ) ->
            ( model, read f )

        ( DecodeFile s, Empty ) ->
            ( fileStringToModel s, Cmd.none )

        ( _, _ ) ->
            ( model, Cmd.none )


requestJson : Cmd Msg
requestJson =
    file [ "application/json", "text/json" ] DataLoaded



--fullDecoder : Decoder({  })


type alias CardsAndMat =
    { distanceMatrix : Array (Array Float)
    , cards : Array Card
    }


fullDecoder : Decoder CardsAndMat
fullDecoder =
    Decode.map2 CardsAndMat
        diffMatrixDecoder
        cardListDecoder


diffMatrixDecoder : Decoder (Array (Array Float))
diffMatrixDecoder =
    field "distMat" (Decode.array (Decode.array Decode.float))


cardListDecoder : Decoder (Array Card)
cardListDecoder =
    field "cards" (Decode.array cardDecoder)


cardDecoder : Decoder Card
cardDecoder =
    Decode.map2 Card
        (field "name" Decode.string)
        (field "imgUrl" Decode.string)


read : File -> Cmd Msg
read f =
    Task.perform DecodeFile (File.toString f)


fileStringToModel : String -> Model
fileStringToModel fileString =
    case decodeString fullDecoder fileString of
        Ok cnm ->
            ShowCards
                { currentCard = Nothing
                , data = D.createData cnm.distanceMatrix cnm.cards
                }

        Err e ->
            --log (toString e) (Broken "Failed to decode your json file. Please try reseting and uploading another file.")
            Broken "Failed to decode your json file. Please try reseting and uploading another file."



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW


view : Model -> Html Msg
view model =
    let
        mainDisplay =
            case model of
                Empty ->
                    div []
                        [ text "currently empty"
                        , button [ onClick RequestData ] [ text "Load Data" ]
                        ]

                ShowCards m ->
                    case m.currentCard of
                        Nothing ->
                            displayCardList m.data

                        Just i ->
                            displayRow i m.data

                Broken s ->
                    text <| String.concat [ "ERROR: ", s ]
    in
    div []
        [ mainDisplay
        , div [] [ button [ onClick Reset ] [ text "Reset" ] ]
        , div [] [ text "CSC 664 final project Kevin & Aaron" ]
        , div []
            [ a [ href "https://github.com/SudoSanauu/Multimedia-Project-CSC664_FinalProject_Group8" ]
                [ text "Project Link" ]
            ]
        ]


displayCardList : Data -> Html Msg
displayCardList d =
    let
        f i card =
            div [ onClick (SetCard i), style "display" "inline-block" ]
                [ C.display card ]
    in
    div [] (A.toList <| A.indexedMap f d.cardList)


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
    div [ onClick Reset ]
        [ text "ERROR: Something went wrong where it shouldn't have, please click this text to reset the app." ]
