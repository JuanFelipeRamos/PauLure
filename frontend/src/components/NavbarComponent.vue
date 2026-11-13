<template>
    <nav>
        <p>PauLure</p>

        <ul>
            <li>Inicio</li>
            <li>Catálogo</li>
            <li>Sobre nosotros</li>
            <li>Contacto</li>
        </ul>

        <input type="text" placeholder="Busca productos aquí">
    </nav>
</template>

<style scoped>
@import url('https://googleapis.com');

nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0px 17px;
}

p {
    font-size: 24px;
    color: #5D1133;
}

ul {
    padding: 0%;
    display: flex;
    justify-content: space-between;
}

li {
    list-style: none;
    margin: 0px 15px;
    color: rgb(114, 114, 114);
    font-size: 15px;
    font-family: 'Plus Jakarta Sans', sans-serif;
    transition: 0.5s;
}

input {
    width: 210px;
    height: 25px;
    padding-left: 14px;
    border: solid 1px rgb(219, 219, 219);
    border-radius: 8px;
    background-color: rgb(250, 250, 250);
}

input::placeholder {
    font-size: 13px;
    color: rgb(148, 148, 148);
}

li:hover {
    color: rgb(114, 18, 18);
    cursor: pointer;
}

</style>