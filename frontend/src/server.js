const prod = `${window.location.protocol}//${window.location.host}/`;
const dev = "http://localhost:8000/";
const serverUrl = process.env.NODE_ENV === "development" ? dev : prod;
export default serverUrl;
