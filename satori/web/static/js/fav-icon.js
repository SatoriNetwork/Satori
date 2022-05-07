function toggle_fav(item) {
  if(item.href.includes("/make_favorite/")){
    item.href = item.href.replace("/make_favorite/", "/remove_favorite/");
    item.classList.remove('honey-text');
    item.classList.add('grey-text');
    item.classList.add('text-darken-1');
    item.innerHTML = "<i class='material-icons'>star_border</i>";
  } else {
    item.href = item.href.replace("/remove_favorite/", "/make_favorite/");
    item.classList.remove('grey-text');
    item.classList.remove('text-darken-1');
    item.classList.add('honey-text');
    item.innerHTML = "<i class='material-icons'>star</i>";
  }
}
