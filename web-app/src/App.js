import React, { useEffect } from "react";
import "./App.css";
import Header from "./components/Header";
import Home from "./components/Home";
import Songs from "./components/Songs"
import { AppStateContext } from "./helpers/Context";

export default function App() {
  const [token, setToken] = React.useState("")
  const [menuState, setMenuState] = React.useState("Home")
  const [recommendedSongs, setRecommendedSongs] = React.useState([])

  useEffect(() => {
    const fetchToken = async () => {
      const result = await authorize();
      setToken(result);
    };

    fetchToken();
  }, []);

  const authorize = async () => {
    const result = await fetch('https://accounts.spotify.com/api/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic ' + btoa(process.env.REACT_APP_CLIENT_ID + ':' + process.env.REACT_APP_CLIENT_SECRET)
      },
      body: 'grant_type=client_credentials'
    });

    const data = await result.json();
    return data.access_token;
  }

  return (
    <div className="App">
      <AppStateContext.Provider
        value={{
          menuState,
          setMenuState,
          recommendedSongs,
          setRecommendedSongs
        }}
      >
        <Header />
        {menuState === "Home" && <Home token={token} />}
        {menuState === "Songs" && <Songs />}
      </AppStateContext.Provider>
    </div>
  );
}
