let themeSetLight = document.querySelector("#themeSetLight");
let themeSetDark = document.querySelector("#themeSetDark");
themeSetLight.addEventListener('click', function(){
    // console.log("l");
    document.cookie = `theme=light; path=/; max-age=${1000*60*60*24*90}`;
    applyTheme();
});
themeSetDark.addEventListener('click', function(){
    // console.log("d");
    document.cookie = `theme=dark; path=/; max-age=${1000*60*60*24*90}`;
    applyTheme();
});