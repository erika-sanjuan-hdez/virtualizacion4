# Sistema distribuido para registros de Personas 

Este proyecto despliega y configura automáticamente un **entorno de infraestructura como código (IaC)** utilizando **Vagrant** para el aprovisionamiento de máquinas virtuales (VMs) y **Ansible** para la automatización de la configuración y el despliegue de servicios.

---

## Componentes de la Infraestructura

El entorno está compuesto por tres máquinas virtuales interconectadas, cada una con un rol específico:

* **`app-server`**: Actúa como el **nodo de control de Ansible**, desde donde se gestiona centralizadamente la configuración del resto de las VMs. Además, está diseñado para alojar la aplicación web principal.
* **`dns-server`**: Funciona como un **servidor DNS interno**, lo que permite que las VMs se comuniquen entre sí utilizando nombres de host fáciles de recordar en lugar de direcciones IP, simplificando la conectividad dentro del entorno.
* **`db-server`**: Aloja un **servidor de base de datos PostgreSQL**, ejecutándose como un contenedor Docker orquestado mediante `docker-compose`. Esta VM es la capa de persistencia de datos esencial para la aplicación.

---

## Flujo de Trabajo y Automatización

1.  **Aprovisionamiento Inicial con Vagrant**:
    Vagrant se encarga de crear las máquinas virtuales, instalar el sistema operativo base (Ubuntu) y el software fundamental necesario en cada una. Esto incluye la instalación de Docker en `db-server` y Python con sus herramientas de entorno virtual en `app-server`.
2.  **Configuración y Despliegue con Ansible**:
    Una vez que las VMs están en funcionamiento, Ansible, ejecutado desde el `app-server`, toma el control para automatizar la configuración detallada:
    * Establece la comunicación segura entre todas las VMs mediante la gestión de claves SSH.
    * Configura el servidor DNS en `dns-server` para la resolución de nombres interna.
    * Prepara el entorno de Docker en `db-server`, asegurando que todas las dependencias Python necesarias para la interacción con Docker estén instaladas, y finalmente, despliega y gestiona el contenedor de PostgreSQL.

---

## Beneficios del Enfoque IaC

Adoptar esta metodología de Infraestructura como Código ofrece múltiples ventajas:

* **Reproducibilidad**: Permite recrear el entorno completo de forma idéntica y consistente en cualquier momento y en cualquier máquina que ejecute Vagrant.
* **Consistencia**: Garantiza que todas las VMs y servicios estén configurados de la misma manera, minimizando los errores humanos y las desviaciones de configuración.
* **Agilidad en el Desarrollo**: Acelera significativamente la configuración de entornos de desarrollo y prueba, facilitando un ciclo de vida de desarrollo más rápido y eficiente.
* **Simulación de Entornos Reales**: Proporciona un entorno controlado para simular despliegues en producción, permitiendo probar la configuración antes de la implementación real.

---

## Pasos para Levantar el Entorno

Sigue estos pasos para desplegar y configurar el entorno completo:

### 1. Generar Par de Llaves SSH para Ansible

Antes de iniciar las VMs, genera el par de llaves SSH que Ansible usará para comunicarse con `dns-server` y `db-server` desde `app-server`. Asegúrate de ejecutar este comando **en tu máquina host** (en la raíz de tu proyecto donde se encuentra el `Vagrantfile`).

Ejecuta `ssh-keygen` sin el argumento de la contraseña. Cuando te pida una contraseña, **simplemente presiona Enter dos veces** para dejarla vacía:

```bash
ssh-keygen -t ed25519 -f private_keys/ansible_id_ed25519
```

Verás las siguientes indicaciones, donde solo debes presionar `Enter`:

```
Enter passphrase (empty for no passphrase): [Presiona Enter aquí]
Enter same passphrase again: [Presiona Enter aquí]
```

> **Nota**: Este comando creará las llaves `ansible_id_ed25519` (privada) y `ansible_id_ed25519.pub` (pública) dentro del directorio `private_keys/` de tu proyecto. **Es fundamental que la llave privada no tenga contraseña** para que la automatización con Ansible funcione correctamente.


### 2. Creación y Configuración Inicial de las VMs

Asegúrate de estar en el directorio raíz de tu proyecto donde se encuentra el `Vagrantfile` y ejecuta:

```bash
vagrant up
```
> **Nota**: Este comando creará y provisionará las tres máquinas virtuales (`app-server`, `dns-server`, `db-server`). El proceso puede tardar unos minutos dependiendo de tu conexión a internet y los recursos del sistema.

### 3. Conectarse a `app-server` (Controlador de Ansible)

Una vez que las VMs estén levantadas, conéctate a la `app-server`, que actuará como tu nodo de control para ejecutar los playbooks de Ansible:

```bash
vagrant ssh app-server
```
> **A partir de este punto, todos los comandos de Ansible se ejecutarán desde la terminal de `app-server`.**

### 4. Preparación de `app-server` para Ansible

Dentro de `app-server`, actualiza las dependencias e instala Ansible:

```bash
sudo apt update
sudo apt install -y ansible
```

### 5. Navegar al Directorio de Playbooks

Cambia al directorio donde se encuentran tus playbooks de Ansible. Este directorio suele estar sincronizado desde tu máquina host.

```bash
cd /vagrant/ansible
```

### 6. Validar la Versión de Ansible

Puedes verificar que Ansible se instaló correctamente:

```bash
ansible --version
```

### 7. Ejecutar los Playbooks de Ansible

Ahora, ejecuta cada playbook en el orden especificado para configurar los diferentes componentes de tu infraestructura:

#### 7.1. Ejecutar Configuración Inicial (SSH Keys)

```bash
ansible-playbook playbooks/initial_setup.yml
```

#### 7.2. Ejecutar Configuración DNS

```bash
ansible-playbook playbooks/dns_setup.yml
```

#### 7.3. Ejecutar Configuración de Base de Datos (PostgreSQL en Docker)

```bash
ansible-playbook playbooks/db_setup.yml
```

#### 7.4. Ejecutar Configuración de Aplicación

```bash
ansible-playbook playbooks/app_setup.yml
```

---

## Pruebas de la Aplicación (Desde tu máquina host)

Una vez que todos los playbooks se hayan ejecutado exitosamente, tu aplicación debería estar corriendo en `app-server` y accesible desde tu máquina **host** (Windows CMD en este caso) a través del puerto mapeado (`localhost:5000`).

### 1. Probar Endpoint GET (Listar Registros)

Abre una nueva terminal en tu máquina **host** (CMD de Windows) y ejecuta:

```bash
curl http://localhost:5000/personas
```

### 2. Probar Endpoint POST (Agregar Nuevo Registro)

Desde tu terminal de host, ejecuta este comando para añadir un nuevo registro:

```bash
curl -X POST -H "Content-Type: application/json" -d "{\"nombre\": \"Ana\", \"apellido\": \"Gonzales\", \"email\": \"ana.gonzales@unam.com\", \"password_hash\": \"another_secure_hash\"}" http://localhost:5000/personas
```
