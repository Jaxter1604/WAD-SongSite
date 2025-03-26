document.addEventListener("DOMContentLoaded", function () {
    let searchInput = document.getElementById('search-input');
    let resultsDiv = document.getElementById('search-results');

    searchInput.addEventListener('input', function () {
        let query = searchInput.value.trim();

        if (query.length < 2) {
            resultsDiv.innerHTML = "";
            return;
        }

        fetch(`/songeek/search/api/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                let output = "<h2>Search Results</h2>";

                if (data.albums.length || data.songs.length) {
                    if (data.albums.length) {
                        output += "<h3>Albums</h3><ul>";
                        data.albums.forEach(album => {
                            output += `<li><a href="/album/${album.slug}/">${album.name} by ${album.artist}</a></li>`;
                        });
                        output += "</ul>";
                    }

                    if (data.songs.length) {
                        output += "<h3>Songs</h3><ul>";
                        data.songs.forEach(song => {
                            output += `<li><a href="/song/${song.id}/">${song.title}</a></li>`;
                        });
                        output += "</ul>";
                    }
                } else {
                    output += "<p>No results found.</p>";
                }

                resultsDiv.innerHTML = output;
            })
            .catch(error => console.error("Error fetching search results:", error));
    });
});
