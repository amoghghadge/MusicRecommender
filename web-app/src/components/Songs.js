import React, { useContext } from "react";
import "./Home.css";
import { AppStateContext } from "../helpers/Context";

export default function Home(props) {
    const { recommendedSongs } = useContext(AppStateContext)

    return (
        <div>
            <p>These are songs</p>
            {recommendedSongs.map((str, index) => (
                <div key={index}>
                    <p>{str}</p>
                </div>
            ))}
        </div>
    );
}