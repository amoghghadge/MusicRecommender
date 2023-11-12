import React, { useContext } from "react";
import { AppStateContext } from "../helpers/Context";
import Input from "@mui/joy/Input";
import Slider from '@mui/joy/Slider';
import Box from "@mui/joy/Box";
import Button from "@mui/joy/Button";
import warning from "../resources/warning.png";
import "./Home.css";

export default function Home(props) {
  const { setMenuState, setRecommendedSongs } = useContext(AppStateContext);
  const [validLink, setValidLink] = React.useState(false);
  const [triedInputting, setTriedInputting] = React.useState(false);
  const [playlistImage, setPlaylistImage] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [playlistId, setPlaylistId] = React.useState("");
  const [numSongs, setNumSongs] = React.useState(5);

  const handleInputChange = async (event) => {
    const playlist = event.target.value
    const x = playlist.indexOf("playlist/");
    const y = playlist.indexOf("?");

    if (playlist === "") {
      setTriedInputting(false)
      setValidLink(false)
      return
    }

    if (x === -1 || y === -1) {
      setTriedInputting(true)
      setValidLink(false)
      return
    }

    try {
      const id = playlist.substring(x + 9, y)
      setPlaylistId(id)
      const result = await fetch(`https://api.spotify.com/v1/playlists/${id}/images`, {
        method: 'GET',
        headers: { 'Authorization': 'Bearer ' + props.token }
      });

      if (!result.ok) {
        throw new Error(`HTTP error! status: ${result.status}`);
      }

      const data = await result.json();
      setPlaylistImage(data[0].url)
      setValidLink(true)
    } catch (error) {
      setValidLink(false)
    }
    setTriedInputting(true)
  }

  const handleSliderChange = (event, newValue) => {
    setNumSongs(newValue)
  }

  const getRecommendations = async (event) => {
    if (validLink !== true) {
      alert("Enter a valid link!")
      return
    }
    setLoading(true)

    const result = await fetch(`https://api.spotify.com/v1/playlists/${playlistId}/tracks`, {
      method: 'GET',
      headers: { 'Authorization': 'Bearer ' + props.token }
    });

    const data = await result.json()
    let tracks = [];

    for (let track_obj of data.items) {
      try {
        const track = track_obj.track

        var dict = {};
        dict["name"] = track.name;
        dict["year"] = parseFloat(track.album.release_date.substring(0, 4));

        tracks.push(dict);
      } catch {
        continue;
      }
    }

    const lambda = await fetch(`https://2uhqdfqcca.execute-api.us-east-1.amazonaws.com/prod/`, {
      method: 'POST',
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ "Songs": tracks, "Number": numSongs })
    });

    const lamdbaResult = await lambda.json();
    console.log(lamdbaResult)

    setLoading(false)
    // TODO: update list of songs from lambdaResult
    let songs = ["asdf", "haslkdf", "asldjfk"]
    setRecommendedSongs(songs)
    setMenuState("Songs")
  }

  return (
    <div style={{ width: "75%" }}>
      {triedInputting === true && validLink === false &&
        <div>
          <img src={warning} style={{ height: "25vh" }} alt="invalid"></img>
          <p>Invalid link! Make sure the playlist is public!</p>
        </div>}
      {triedInputting === true && validLink === true &&
        <div>
          <img src={playlistImage} style={{ height: "30vh" }} alt="playlist cover"></img>
        </div>}
      <div style={{ marginTop: "5vh" }}>
        <Input
          size="lg"
          variant="outlined"
          placeholder="Enter the link to your spotify playlist..."
          fullWidth={true}
          onChange={handleInputChange}
        />
        <p style={{ fontSize: "1em" }}>Number of songs</p>
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            marginBottom: '2vw'
          }}
        >
          <Slider color="success" variant="solid" valueLabelDisplay="auto" defaultValue={5} min={5} max={25} onChange={handleSliderChange} />
        </Box>
        <Button color="success" size="lg" disabled={!validLink} onClick={getRecommendations} loading={loading}>Get Recommendations</Button>
      </div>
    </div>
  );
}
