export default async function getData() {
    const data = await fetch("http://127.0.0.1:8000/all-data")
    if (!data.ok) throw new Error("Failed to fetch data")
    return data.json()
}