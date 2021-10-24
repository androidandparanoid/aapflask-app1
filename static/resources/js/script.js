function copyUrl(){
    let copyText = document.getElementById("new_url")
    copyText.select()   
    navigator.clipboard.writeText(copyText.value)
    console.log(`Copied text: ${copyText.value}`)
}