// Get the hash of the url
const hash = window.location.hash
  .substring(1)
  .split("&")
  .reduce(function(initial, item) {
    if (item) {
      var parts = item.split("=");
      initial[parts[0]] = decodeURIComponent(parts[1]);
    }
    return initial;
  }, {});
window.location.hash = "";

// Set token
let _token = hash.access_token;
console.log(_token);

const authEndpoint = "https://accounts.spotify.com/authorize";
const clientId = "3f24d8da29c44c2d80b2c2abe518b5d6";
const redirectUri = "http://127.0.0.1:5000/display_playlist"
const scopes = [
    "streaming",
    "user-read-private",
    "user-modify-playback-state",
    "user-read-playback-state",
    "user-library-modify"
];

// If there is no token, redirect to Spotify authorization
if (!_token) {
    window.location = `${authEndpoint}?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scopes.join(
      "%20"
    )}&response_type=token&show_dialog=true`;
  }



// Set up Web Playback SDK
window.onSpotifyPlayerAPIReady = () => {

    // Create Spotify player
    const player = new Spotify.Player({
        name: "Web Playback SDK Template",
        getOAuthToken: cb => {
            cb(_token);
        }
    });

    // Error handling
    player.on("initialization_error", e => console.error(e));
    player.on("authentication_error", e => console.error(e));
    player.on("account_error", e => console.error(e));
    player.on("playback_error", e => console.error(e));

    // Playback status updates
    player.on("player_state_changed", state => {
        console.log(state);
        $("#current-track").attr(
            "src",
            state.track_window.current_track.album.images[0].url
        );
        $("#current-track-name").text(state.track_window.current_track.name);
    });

    // Ready
    player.on("ready", data => {
        console.log("Ready with Device ID", data.device_id);
        //console.log(_token);

        // Play a track using our new device ID
        play(data.device_id);
    });

    player.connect();
};

// This doesn't work == find a way to pass the uri 
/*
var uri1 = '{"uris": [';
var uri2 = '{{ uri }}';
var uri3 = ']}';
var final_uri = uri1.concat(uri2, uri3);
console.log(final_uri);s
*/

// Play a specified track on the Web Playback SDK's device ID
function play(device_id) {
    $.ajax({
      url: "https://api.spotify.com/v1/me/player/play?device_id=" + device_id,
      type: "PUT",
      data:
        '{"uris": ["spotify:track:4mIneE97TsDiTsoQkFSDrX"]}',
      beforeSend: function(xhr) {
        xhr.setRequestHeader("Authorization", "Bearer " + _token);
      },
      success: function(data) {
        console.log(data);
      }
    });
  }

