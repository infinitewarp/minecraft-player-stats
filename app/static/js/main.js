playerData = null;
function loadPlayerData(playerName) {
    $.getJSON("/player/" + playerName + ".json", function(data) {
        playerData = data;
        $("#data").text(JSON.stringify(playerData));
    });
}