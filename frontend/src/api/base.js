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

const getResponse = async response => {
  const contentType = response.headers.get("content-type");
  if (contentType === "application/json") {
    const json = await response.json();
    return { response, json };
  }
  return { response };
};

const baseRequest = async (url, method, body, signal) => {
    const response = await fetch(new URL(url, serverUrl), {
        method: method,
        body: body,
        signal: signal,
        credentials: "include",
        headers: {
        "x-csrftoken": getCookie("x-csrftoken"),
        "Content-Type": "application/json"
        }
    });
    const myResponse = await getResponse(response);
    return myResponse.json;
};

export { baseRequest };
