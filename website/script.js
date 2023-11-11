async function authorize() {

    const result = await fetch('https://accounts.spotify.com/api/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + btoa(client_id + ':' + client_secret)
        },
        body: 'grant_type=client_credentials'
    });

    const data = await result.json();
    return data.access_token;

}

async function getPlaylistTracks(playlistId, token) {

    const result = await fetch(`https://api.spotify.com/v1/playlists/${playlistId}/tracks`, {
        method: 'GET',
        headers: { 'Authorization': 'Bearer ' + token }
    });

    const data = await result.json();

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

    console.log("TRACKS: ");
    console.log(tracks);
    return tracks;

}

async function getRecommendations(songs, num) {

    const result = await fetch(`https://2uhqdfqcca.execute-api.us-east-1.amazonaws.com/prod`, {
        method: 'POST',
        statusCode: 200,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ "Songs": songs, "Number": num })
    });

    const data = await result.json();
    return data;

}

async function myFunction() {

    const x = document.getElementById("playlist").value.indexOf("playlist/");
    const y = document.getElementById("playlist").value.indexOf("?");

    const token = await authorize();
    console.log(token)
    // const songs = await getPlaylistTracks(document.getElementById("playlist").value.substring(x + 9, y), token);
    // const num = document.getElementById("numsongs").value;
    // console.log("INPUTTING BODY:");
    // console.log(JSON.stringify({ "Songs": songs, "Number": num }));

    // console.log("GETTING RECOMMENDATIONS:")
    // const recommendations = await getRecommendations(songs, num);
    // document.getElementById("recommendations").innerHTML = JSON.stringify(recommendations);
    // console.log(recommendations);

}