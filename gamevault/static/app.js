async function api(method, url, body) {
  const options = { method, headers: {} };
  if (body !== undefined) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url, options);
  if (response.status === 204) {
    return null;
  }

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || "Something went wrong");
  }
  return data;
}

function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = value;
  return div.innerHTML;
}

function formatDate(value) {
  return new Date(value.replace(" ", "T") + "Z").toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function formatPrice(price) {
  return price === 0 ? "Free" : `$${price.toFixed(2)}`;
}

function showAlert(container, message, type = "danger") {
  container.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      ${escapeHtml(message)}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>`;
}

function platformBadges(platforms) {
  return platforms
    .map((name) => `<span class="badge text-bg-dark border me-1">${escapeHtml(name)}</span>`)
    .join("");
}

function gameImage(game, className) {
  if (game.image_url) {
    const fit = game.image_url.endsWith("#contain") ? " fit-contain" : "";
    return `<img src="${escapeHtml(game.image_url)}" alt="${escapeHtml(game.title)}" class="${className}${fit}" loading="lazy">`;
  }
  return `<div class="${className} game-image-placeholder">${escapeHtml(game.title.charAt(0))}</div>`;
}

function tagBadges(tags) {
  return tags
    .map((tag) => `<a href="/?tag=${encodeURIComponent(tag.name)}" class="badge text-bg-secondary text-decoration-none me-1">${escapeHtml(tag.name)}</a>`)
    .join("");
}

function steamSummary(summary) {
  const plural = (count, word) => `${count} ${word}${count === 1 ? "" : "s"}`;
  let message = `Imported from Steam: ${plural(summary.added_to_library, "game")} added to the library`;
  if (summary.new_catalog_games) {
    message += `, ${plural(summary.new_catalog_games, "new game")} added to the catalog`;
  }
  message += ".";
  if (summary.not_imported_yet) {
    message += ` ${summary.not_imported_yet} more can be imported by running the import again.`;
  }
  return message;
}

function storeUrl(platform, game) {
  const title = encodeURIComponent(game.title);
  switch (platform) {
    case "Steam":
      return game.steam_app_id
        ? `https://store.steampowered.com/app/${game.steam_app_id}`
        : `https://store.steampowered.com/search/?term=${title}`;
    case "Epic Games Store":
      return `https://store.epicgames.com/en-US/browse?q=${title}`;
    case "PlayStation Store":
      return `https://store.playstation.com/en-us/search/${title}`;
    case "Xbox Store":
      return `https://www.xbox.com/en-US/search/results/games?q=${title}`;
    case "Nintendo eShop":
      return `https://www.nintendo.com/us/search/#q=${title}`;
    default:
      return `https://www.google.com/search?q=${encodeURIComponent(`${game.title} ${platform}`)}`;
  }
}

document.getElementById("logout")?.addEventListener("click", async () => {
  await api("POST", "/api/logout");
  window.location = "/";
});
