import serverUrl from "../server";

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function setCookie(name,value,days) {
  var expires = "";
  if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days*24*60*60*1000));
      expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

const getResponse = async response => {
  const contentType = response.headers.get("content-type");
  if (contentType === "application/json") {
    const json = await response.json();
    return { response, json };
  }
  if (contentType === 'application/pdf'){
    response.blob().then(
      (blob) =>{
        const url = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `export.pdf`);
        document.body.appendChild(link);
        link.click();
        link.parentNode.removeChild(link);
      }
    )
    const json = {'status':true}
    return {response, json}
  }
  return { response };
};

const baseRequest = async (url, method, body, signal) => {
    var cookie = getCookie("x-csrftoken")
    if (cookie === null) {
      const response = await fetch(new URL('apiv1/users/verify', serverUrl), {
        method: 'GET'
      });
      const temp = await getResponse(response)
      setCookie('x-csrftoken', temp.json['x-csrftoken'], 2)
    }
    cookie = getCookie("x-csrftoken")
    const response = await fetch(new URL(url, serverUrl), {
        method: method,
        body: body,
        signal: signal,
        credentials: "include",
        headers: {
        "x-csrftoken": cookie,
        "Content-Type": "application/json"
        }
    });
    const myResponse = await getResponse(response);
    return myResponse.json;
};


export { baseRequest };