<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faEye, faEyeSlash } from '@fortawesome/free-solid-svg-icons'
import api from '@/services/axios';

const router = useRouter()

const username = ref('');
const password = ref('');

const login = async () => {
  try {
    const response = await api.post("/token/", {
      "username": username.value,
      "password": password.value
    });

    localStorage.setItem("access", response.data.access);
    localStorage.setItem("refresh", response.data.refresh);

    console.log("inicio de sesión exitoso");

    username.value = "";
    password.value = "";

    router.push("/homepaneladmin");
  } catch (error) {
    alert("error al iniciar sesión")
    console.log("error: ", error);
  }
}

const mostrarContrasena = ref(false)

</script>

<template>
  <section class="login" aria-labelledby="login-titulo">
    <article class="login__card">
      <header class="login__header">
        <h1 id="login-titulo" class="login__titulo">
          Acceso al Panel de
          <br>
          Administración
        </h1>
      </header>

      <form class="login__form" @submit.prevent="login">
        <div class="campo">
          <label class="campo__label" for="usuario">Nombre de usuario</label>
          <div class="campo__control">
            <font-awesome-icon class="campo__icono" icon="fa-solid fa-envelope" fixed-width aria-hidden="true" />
            <input
              id="usuario"
              class="campo__input"
              type="text"
              name="usuario"
              placeholder="adminPL123"
              autocomplete="username"
              required
              v-model="username"
            />
          </div>
        </div>

        <div class="campo">
          <label class="campo__label" for="contrasena">Contraseña</label>
          <div class="campo__control">
            <font-awesome-icon class="campo__icono" icon="fa-solid fa-lock" fixed-width aria-hidden="true" />
            <input
              id="contrasena"
              class="campo__input campo__input--con-accion"
              :type="mostrarContrasena ? 'text' : 'password'"
              name="contrasena"
              autocomplete="current-password"
              required
              v-model="password"
            />
            <button
              class="campo__accion"
              type="button"
              :aria-label="mostrarContrasena ? 'Ocultar contraseña' : 'Mostrar contraseña'"
              :aria-pressed="mostrarContrasena"
              @click="mostrarContrasena = !mostrarContrasena"
            >
              <FontAwesomeIcon :icon="mostrarContrasena ? faEyeSlash : faEye" aria-hidden="true" />
            </button>
          </div>
        </div>

        <button class="login__boton" type="submit">Iniciar sesión</button>
      </form>
    </article>
  </section>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap');

.login {
  --fondo: #fff6fb;
  --mancha: #ffe3ec;
  --vino: #7b2848;
  --vino-oscuro: #5c1238;
  --campo-fondo: #f9f0f3;
  --texto-suave: #8a6b79;
  --texto-label: #4a3a41;

  position: relative;
  overflow: hidden;
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 1rem;
  background: var(--fondo);
  font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
}

/* manchas difuminadas del fondo */
.login::before,
.login::after {
  content: '';
  position: absolute;
  width: 520px;
  height: 520px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 227, 236, 1) 0%, rgba(255, 227, 236, 0) 70%);
  pointer-events: none;
}

.login::before {
  top: -170px;
  right: -160px;
}

.login::after {
  bottom: -154px;
  left: -160px;
}

.login__card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 418px;
  padding: 40px 40px 24px;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 10px 40px rgba(123, 40, 72, 0.08);
}

.login__header {
  margin-bottom: 40px;
}

.login__titulo {
  margin: 0;
  text-align: center;
  font-family: 'Playfair Display', Georgia, serif;
  font-weight: 500;
  font-size: 1.75rem;
  line-height: 1.25;
  color: var(--vino-oscuro);
}

.login__form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.campo__label {
  display: block;
  margin-bottom: 4px;
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--texto-label);
}

.campo__control {
  position: relative;
}

.campo__input {
  width: 100%;
  height: 48px;
  padding: 0 16px 0 40px;
  border: 2px solid transparent;
  border-radius: 12px;
  background: var(--campo-fondo);
  font: inherit;
  font-size: 1rem;
  color: var(--vino-oscuro);
  box-sizing: border-box;
  transition: border-color 0.2s, background 0.2s;
}

.campo__input--con-accion {
  padding-right: 48px;
}

.campo__input::placeholder {
  color: var(--texto-suave);
}

.campo__input:focus-visible {
  outline: none;
  border-color: var(--vino);
  background: #fff;
}

.campo__icono {
  position: absolute;
  top: 50%;
  left: 9px;
  width: 18px;
  height: 18px;
  transform: translateY(-50%);
  font-size: 16px;
  color: var(--texto-suave);
  pointer-events: none;
}

.campo__accion {
  position: absolute;
  top: 50%;
  right: 12px;
  display: grid;
  place-items: center;
  width: 28px;
  height: 28px;
  padding: 0;
  transform: translateY(-50%);
  border: 0;
  border-radius: 8px;
  background: transparent;
  cursor: pointer;
}

.campo__accion svg {
  font-size: 16px;
  color: var(--texto-suave);
}

.campo__accion:focus-visible {
  outline: 2px solid var(--vino);
}

.login__boton {
  height: 52px;
  border: 0;
  border-radius: 12px;
  background: var(--vino);
  font: inherit;
  font-size: 0.875rem;
  font-weight: 500;
  color: #fff;
  cursor: pointer;
  transition: background 0.2s;
}

.login__boton:hover {
  background: var(--vino-oscuro);
}

.login__boton:focus-visible {
  outline: 3px solid rgba(123, 40, 72, 0.35);
  outline-offset: 2px;
}

</style>