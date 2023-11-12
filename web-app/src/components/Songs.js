import React, { useContext, useState, useEffect } from "react";
import "./Home.css";
import { AppStateContext } from "../helpers/Context";
import Link from '@mui/joy/Link';

export default function Songs(props) {
    const { recommendedSongs } = useContext(AppStateContext)
    const [topText, setTopText] = useState("")

    useEffect(() => {
        const temp = recommendedSongs.length === 0 ? "Fill out the home page to get recommended songs!" : "These are your recommended songs!"
        setTopText(temp)
    }, [recommendedSongs.length]);

    return (
        <div style={{ marginBottom: "10vh" }}>
            <p style={{ marginBottom: "5vh" }}>{topText}</p>
            {recommendedSongs.map(song => (
                <div style={{ display: "flex", flexDirection: "row", gap: "5vw", alignItems: "center", marginBottom: "3vh", marginLeft: "3vw", marginRight: "3vw" }} key={song.name}>
                    <img src={song.image_url} style={{ height: "18vh" }} alt="song cover"></img>
                    <Link level="title-lg" href={song.url} target="_blank" rel="noopener noreferrer">{song.name} by {song.artists}</Link>
                </div>
            ))}
        </div>
    );
}