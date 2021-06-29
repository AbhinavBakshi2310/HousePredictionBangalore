mybutton = document.getElementById("summarized");
mybutton.onclick = e => {
    e.preventDefault();
    document.getElementById('text-here').innerHTML = "Loading...   It may take some time. Please keep this window active until then.";
    chrome.tabs.query({active: true, currentWindow: true}, tabs => {
        chrome.tabs.sendMessage(tabs[0].id, {action:"load_summary"});
            var url = tabs[0].url;
            let xhr = new XMLHttpRequest();
            xhr.addEventListener("load",function createtext(){
                chrome.tabs.sendMessage(tabs[0].id, {action:"print_summary", summary: this.responseText});
            }); 
            xhr.open("GET", 'https://555f247bef61.ngrok.io/api/summarize?youtube_url='+url);
            xhr.send();
            });
}

