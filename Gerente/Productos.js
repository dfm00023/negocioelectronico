let products = [];

async function fetchProducts(){
    try{
        const response = await fetch("https://smartshopdb.xerone.es/modelos");
        data = await response.json();
        products = data.data;
        displayProducts();
    } catch (error){
        console.error("Error al obtener productos:", error);
    }
}