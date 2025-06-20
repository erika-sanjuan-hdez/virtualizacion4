# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Configuración común para todas las máquinas
  config.vm.box = "ubuntu/jammy64" # Ubuntu 22.04 LTS
  config.ssh.insert_key = true # Genera una clave SSH específica para este proyecto y la coloca en ./.vagrant/machines/<vm_name>/virtualbox/private_key
  config.vm.synced_folder ".", "/vagrant", mount_options: ["dmode=00755", "fmode=00600"]


  
  # Definición del dns-server
  config.vm.define "dns-server" do |dns|
    dns.vm.hostname = "dns-server"
    dns.vm.network "private_network", ip: "192.168.56.12"
    dns.vm.provider "virtualbox" do |vb|
      vb.name = "dns-server"
      vb.memory = "1024"
      vb.cpus = "1"
    end

    dns.vm.provision "shell", inline: <<-SHELL
      # 1. Asegura que el directorio .ssh exista y tenga los permisos correctos
      mkdir -p /home/vagrant/.ssh
      chmod 700 /home/vagrant/.ssh

      # 2. *** ESTA ES LA LÍNEA CLAVE PARA AGREGAR LA LLAVE PRIVADA ***
      #    Reemplaza [RUTA_ORIGEN_EN_HOST] con la ruta correcta en tu máquina host
      #    Por ejemplo, /vagrant/private_keys/ansible_id_ed25519
      cp /vagrant/private_keys/ansible_id_ed25519 /home/vagrant/.ssh/ansible_id_ed25519
      
      # 3. Asigna los permisos correctos a la llave privada (muy importante para SSH)
      chmod 600 /home/vagrant/.ssh/ansible_id_ed25519

      # 4. Copia la CLAVE PÚBLICA a authorized_keys de app-server (para que app-server pueda aceptarse a sí mismo)
      #    Reemplaza [RUTA_ORIGEN_EN_HOST].pub con la ruta correcta
      cat /vagrant/private_keys/ansible_id_ed25519.pub >> /home/vagrant/.ssh/authorized_keys
      chmod 600 /home/vagrant/.ssh/authorized_keys

      # 5. Asegura que los archivos SSH pertenezcan al usuario vagrant
      chown -R vagrant:vagrant /home/vagrant/.ssh
    SHELL

    # Provisionamiento inicial (instalación de bind9 si no se hace con Ansible en el Vagrantfile)
    # Mejor usar Ansible para todo el provisioning después de que la VM esté levantada.
  end

  # Definición del db-server
  config.vm.define "db-server" do |db|
    db.vm.hostname = "db-server"
    db.vm.network "private_network", ip: "192.168.56.10"
    db.vm.provider "virtualbox" do |vb|
      vb.name = "db-server"
      vb.memory = "1024"
      vb.cpus = "1"
    end

    db.vm.provision "shell", inline: <<-SHELL
      # 1. Asegura que el directorio .ssh exista y tenga los permisos correctos
      mkdir -p /home/vagrant/.ssh
      chmod 700 /home/vagrant/.ssh

      # 2. *** ESTA ES LA LÍNEA CLAVE PARA AGREGAR LA LLAVE PRIVADA ***
      #    Reemplaza [RUTA_ORIGEN_EN_HOST] con la ruta correcta en tu máquina host
      #    Por ejemplo, /vagrant/private_keys/ansible_id_ed25519
      cp /vagrant/private_keys/ansible_id_ed25519 /home/vagrant/.ssh/ansible_id_ed25519
      
      # 3. Asigna los permisos correctos a la llave privada (muy importante para SSH)
      chmod 600 /home/vagrant/.ssh/ansible_id_ed25519

      # 4. Copia la CLAVE PÚBLICA a authorized_keys de app-server (para que app-server pueda aceptarse a sí mismo)
      #    Reemplaza [RUTA_ORIGEN_EN_HOST].pub con la ruta correcta
      cat /vagrant/private_keys/ansible_id_ed25519.pub >> /home/vagrant/.ssh/authorized_keys
      chmod 600 /home/vagrant/.ssh/authorized_keys

      # 5. Asegura que los archivos SSH pertenezcan al usuario vagrant
      chown -R vagrant:vagrant /home/vagrant/.ssh
    SHELL

    # Provisionamiento inicial (instalación de Docker)
    db.vm.provision "shell", inline: <<-SHELL
      echo "Instalando Docker en db-server..."
      sudo apt update && sudo apt install -y apt-transport-https ca-certificates curl software-properties-common gnupg-agent
      curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
      echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
      sudo apt update
      sudo apt install -y docker-ce docker-ce-cli containerd.io
      sudo usermod -aG docker vagrant

      sudo systemctl enable docker  # Asegura que Docker inicie con el sistema
      sudo systemctl start docker   # Inicia el servicio Docker (si no está ya corriendo)

      echo "Instalando Docker Compose Plugin..."
      sudo apt update
      sudo apt install -y docker-compose-plugin # Instala la versión más reciente del plugin oficial
      echo "Docker Compose Plugin instalado."

      echo "Docker instalado en db-server."
    SHELL
  end

  # Definición del app-server
  config.vm.define "app-server" do |app|
    app.vm.hostname = "app-server"
    app.vm.network "private_network", ip: "192.168.56.11"

    # Para acceder http://localhost:5000 desde tu máquina host.
    app.vm.network "forwarded_port", guest: 5000, host: 5000
	# app.vm.synced_folder ".", "/vagrant", disabled: false
    app.vm.provider "virtualbox" do |vb|
      vb.name = "app-server"
      vb.memory = "1024"
      vb.cpus = "1"
    end

    app.vm.provision "shell", inline: <<-SHELL
      # 1. Asegura que el directorio .ssh exista y tenga los permisos correctos
      mkdir -p /home/vagrant/.ssh
      chmod 700 /home/vagrant/.ssh

      # 2. *** ESTA ES LA LÍNEA CLAVE PARA AGREGAR LA LLAVE PRIVADA ***
      #    Reemplaza [RUTA_ORIGEN_EN_HOST] con la ruta correcta en tu máquina host
      #    Por ejemplo, /vagrant/private_keys/ansible_id_ed25519
      cp /vagrant/private_keys/ansible_id_ed25519 /home/vagrant/.ssh/ansible_id_ed25519
      
      # 3. Asigna los permisos correctos a la llave privada (muy importante para SSH)
      chmod 600 /home/vagrant/.ssh/ansible_id_ed25519

      # 4. Copia la CLAVE PÚBLICA a authorized_keys de app-server (para que app-server pueda aceptarse a sí mismo)
      #    Reemplaza [RUTA_ORIGEN_EN_HOST].pub con la ruta correcta
      cat /vagrant/private_keys/ansible_id_ed25519.pub >> /home/vagrant/.ssh/authorized_keys
      chmod 600 /home/vagrant/.ssh/authorized_keys

      # 5. Asegura que los archivos SSH pertenezcan al usuario vagrant
      chown -R vagrant:vagrant /home/vagrant/.ssh
    SHELL

    # Provisionamiento inicial (instalación de Python)
    app.vm.provision "shell", inline: <<-SHELL
      echo "Instalando Python en app-server..."
      sudo apt update
      sudo apt install -y python3 python3-pip python3-venv
      echo "Python y pip instalados en app-server."
    SHELL
  end

  # Integración de Ansible (opcional, puedes ejecutar Ansible manualmente después)
  # Este bloque ejecutará los playbooks de Ansible después de que todas las VMs estén levantadas.
  # Asegúrate de que tu inventario de Ansible esté configurado correctamente.
  ##config.vm.provision "ansible" do |ansible|
  ##  ansible.playbook = "ansible/playbooks/initial_setup.yml" # Playbook inicial para todos
  ##  ansible.extra_vars = {
      # Puedes pasar variables a Ansible si es necesario
  ##  }
    # Si quieres ejecutar playbooks específicos por host o grupo, puedes añadir más bloques de provisionamiento
    # o usar un solo playbook maestro que incluya los otros.
  ##  ansible.playbook = "ansible/playbooks/dns_setup.yml"
  ##  ansible.playbook = "ansible/playbooks/db_setup.yml"
  ##  ansible.playbook = "ansible/playbooks/app_setup.yml"
    # Es mejor tener un playbook maestro que importe los otros o ejecutarlos en orden manual
    # Para el primer setup, recomiendo ejecutarlos manualmente después de 'vagrant up'
  ##end
end