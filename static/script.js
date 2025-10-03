document.getElementById("search-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  // Get form values
  const query = document.getElementById("query").value;
  const min_price = document.getElementById("min_price").value || 0;
  const max_price = document.getElementById("max_price").value || 10000;
  const location = document.getElementById("location").value;
  const listing_type = document.getElementById("listing_type").value;
  const tcg_price_flag = document.getElementById("fetch_tcg_price_flag").checked;

  // Clear previous results
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "<p>Loading results...</p>";

  try {
    const response = await fetch("/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, min_price, max_price, listing_type, location, fetch_tcg_price_flag })
    });

    const data = await response.json();
    resultsDiv.innerHTML = "";

    if (!data.length) {
      resultsDiv.innerHTML = "<p>No results found.</p>";
      return;
    }

    data.forEach(item => {
      const card = document.createElement("div");
      card.classList.add("card");

      card.innerHTML = `
        <img src="${item.image || 'https://via.placeholder.com/225'}" alt="Image">
        <div class="card-content">
          <h2><a href="${item.url}" target="_blank">${item.title}</a></h2>
          <p><strong>eBay Price:</strong> ${item.ebay_price || 'N/A'} ${item.currency || ''}</p>
          ${item.tcg_price_flag ? `<p><strong>TCG Price:</strong> ${item.tcg_price_flag}</p>` : ""}
          ${item.discount ? `<p><strong>Discount vs TCG:</strong> ${item.discount}%</p>` : ""}
          <p><strong>Condition:</strong> ${item.condition || 'N/A'}</p>
          <p><strong>Location:</strong> ${item.location || 'Unknown'}</p>

          ${item.extract_item_specifics && Object.keys(item.extract_item_specifics).length > 0 ? `
            <details>
              <summary>Item extract_item_specifics</summary>
              <ul>
                ${Object.entries(item.extract_item_specifics)
                  .map(([key, value]) => `<li><strong>${key}:</strong> ${value}</li>`)
                  .join("")}
              </ul>
            </details>
          ` : ""}
        </div>
      `;

      resultsDiv.appendChild(card);
    });
  } catch (error) {
    console.error(error);
    resultsDiv.innerHTML = "<p>Error fetching results. Try again.</p>";
  }
});
