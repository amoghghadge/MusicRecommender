import React from "react";
import Box from "@mui/joy/Box";
import IconButton from "@mui/joy/IconButton";
import Menu from "@mui/icons-material/Menu";
import List from "@mui/joy/List";
import ListItem from "@mui/joy/ListItem";
import ListItemButton from "@mui/joy/ListItemButton";
import spotify from "../resources/spotify.png";
import Drawer from "@mui/joy/Drawer";
import "./Header.css";

export default function Header() {
  const [open, setOpen] = React.useState(false);

  const toggleDrawer = (inOpen) => (event) => {
    if (
      event.type === "keydown" &&
      (event.key === "Tab" || event.key === "Shift")
    ) {
      return;
    }

    setOpen(inOpen);
  };

  return (
    <div className="App-header">
      <div style={{ position: "absolute", left: "4vw" }}>
        {/* <Button color="primary" variant="solid" onClick={toggleDrawer(true)}>
          Open drawer
        </Button> */}
        <IconButton
          variant="solid"
          color="neutral"
          size="lg"
          onClick={() => setOpen(true)}
        >
          <Menu />
        </IconButton>
      </div>
      <Drawer open={open} onClose={toggleDrawer(false)} size="sm" anchor="left">
        <Box
          role="presentation"
          onClick={toggleDrawer(false)}
          onKeyDown={toggleDrawer(false)}
        >
          <List>
            {["Home", "Songs", "About"].map((text) => (
              <ListItem key={text}>
                <ListItemButton>{text}</ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>
      <img src={spotify} className="Spotify-logo" alt="spotify" />
      <h2>Music Recommender</h2>
    </div>
  );
}
