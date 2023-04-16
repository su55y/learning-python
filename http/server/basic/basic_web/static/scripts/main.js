const updateTime = async () => {
  const resp = await fetch('/time').then((r) => r.json())
  document.getElementById('time-label').innerText = resp?.time || 'No data'
}

window.onload = () => {
  setInterval(updateTime, 1000)
}
