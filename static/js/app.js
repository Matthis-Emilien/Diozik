const musicContainer = document.getElementById('music-container');

const playBtn = document.getElementById('play');
const volumeBtn = document.getElementById('volume');
const volumeCtrl = document.getElementById('volume-controller');

const audio = document.getElementById('audio');
const progress = document.getElementById('progress');
const progressContainer = document.getElementById('progress-container');
const timeStatus = document.getElementById('current-time');
const durationStatus = document.getElementById('duration');

timeStatus.innerText = "0:00";
durationStatus.innerText = "0:00";

// Update song details
function loadSong(song, link){
    title.innerText = song;
    audio.src = link;
}


// Set Time Info
function currentTimeStatus(e){
    const { duration, currentTime } = e.srcElement;

    let minutes = Math.round(duration / 60);
    let secondes = duration / 60 - minutes;

    if (secondes < 0) {
        secondes = 1 - (secondes - (secondes * 2));
        minutes = minutes - 1
    }

    secondes = secondes * 0.6;

    if (secondes >= 0.595) {
        secondes = 0;
        minutes = minutes + 1;
    }
    minutes = minutes.toString()
    secondes = secondes * 100
    secondesDisplay = secondes.toFixed(0).toString()
    if (secondes.toFixed(0) < 10){
        secondesDisplay = "0" + secondesDisplay
    }
    let convertDuration = minutes + ":" + secondesDisplay;

    let min = Math.round(currentTime / 60);
    let sec = currentTime / 60 - min;

    if (sec < 0) {
        sec = 1 - (sec - (sec * 2));
        min = min - 1
    }

    sec = sec * 0.6;

    if (sec >= 0.595) {
        sec = 0;
        min = min + 1;
    }
    min = min.toString()
    sec = sec * 100
    secDisplay = sec.toFixed(0).toString()
    if (sec.toFixed(0) < 10){
        secDisplay = "0" + secDisplay
    }
    let convertTime = min + ":" + secDisplay;

    timeStatus.innerText = convertTime;
    durationStatus.innerText = convertDuration;
}

// Play Song
function playSong(){
    musicContainer.classList.add("play");
    playBtn.querySelector("i.fas").classList.remove("fa-play");
    playBtn.querySelector('i.fas').classList.add("fa-pause");

    audio.play();
};

// Pause Song
function pauseSong(){
    musicContainer.classList.remove("play");
    playBtn.querySelector("i.fas").classList.add("fa-play");
    playBtn.querySelector('i.fas').classList.remove("fa-pause");

    audio.pause();
}

// Unmute Song
function unmuteSong(){
    audio.volume = 1;

    volumeIcon();
}

// Mute Song
function muteSong(){
    audio.volume = 0;

    volumeIcon();
}

// Update Level Volume
function levelSong(value){
    const lvl = value / 100;
    audio.volume = lvl;

    volumeIcon();
}

// Update Volume Icon
function volumeIcon(){
    if (audio.volume > 0){
        musicContainer.classList.remove("mute");
        volumeBtn.querySelector('i.fas').classList.remove("fa-volume-mute");
        volumeBtn.querySelector("i.fas").classList.add("fa-volume-up");
    } else{
        musicContainer.classList.add("mute");
        volumeBtn.querySelector("i.fas").classList.remove("fa-volume-up");
        volumeBtn.querySelector('i.fas').classList.add("fa-volume-mute");
    }
}

//Update progress bar
function updateProgress(e){
    const { duration, currentTime } = e.srcElement;
    const progressPercent = (currentTime / duration) * 100;
    progress.style.width = `${progressPercent}%`;
}

// Set Progress Bar
function setProgress(e){
    const width = this.clientWidth;
    const clickX = e.offsetX;
    const duration = audio.duration;

    audio.currentTime = (clickX / width) * duration;
}

// End of the song
function endSong(e){
    const progressPercent = 0;
    progress.style.width = `${progressPercent}%`;
    pauseSong();
}

// Event Listener Play button
playBtn.addEventListener('click', () => {
    const isPlaying = musicContainer.classList.contains('play');

    if (isPlaying) {
        pauseSong();
    } else{
        playSong();
    }
});

// Event Listener Volume button
volumeBtn.addEventListener('click', () => {
    const isMute = musicContainer.classList.contains('mute');

    if (isMute) {
        unmuteSong();
    } else{
        muteSong();
    }
});

// Event Listener Volume Level
volumeCtrl.addEventListener('click', () => {
    levelSong(volumeCtrl.value);
});


// Time&Song Update
audio.addEventListener('timeupdate', updateProgress);
audio.addEventListener('timeupdate', currentTimeStatus);

// Click on progress bar
progressContainer.addEventListener("click", setProgress);

// Sond Ends
audio.addEventListener('ended', endSong)