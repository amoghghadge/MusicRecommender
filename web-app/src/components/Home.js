import React from "react";
import Input from "@mui/joy/Input";
import warning from "../resources/warning.png"
import "./Home.css";

export default function Home(props) {
  const [validLink, setValidLink] = React.useState(false);
  const [triedInputting, setTriedInputting] = React.useState(false);
  const [playlistImage, setPlaylistImage] = React.useState("");

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
      setValidLink(false)
      return
    }

    try {
      const id = playlist.substring(x + 9, y)
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

  return (
    <div style={{ width: "75%" }}>
      {triedInputting === true && validLink === false &&
        <div>
          <img src={warning} style={{ height: "35vh" }} alt="invalid"></img>
          <p>Invalid link! Make sure the playlist is public!</p>
        </div>}
      {triedInputting === true && validLink === true &&
        <div>
          <img src={playlistImage} style={{ height: "35vh" }} alt="playlist cover"></img>
          <p>Valid link!</p>
        </div>}
      <div style={{ marginTop: "5vh" }}>
        <Input
          size="lg"
          variant="outlined"
          placeholder="Enter the link to your spotify playlist..."
          fullWidth={true}
          onChange={handleInputChange}
        />
      </div>
    </div>
  );
}
