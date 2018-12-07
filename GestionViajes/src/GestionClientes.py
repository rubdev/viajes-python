# -*- coding: utf-8 -*-


"""
    Gestion de clientes para agencia de viajes
"""


#Importamos las clases sys, pygtk, gtk y gtk.glade
import sys

try:
    import pygtk
    pygtk.require("2.0") 
except:
    print("Error GTK")  
    sys.exit(1)
try:
    import gtk
    import gtk.glade
except:
    print("Error GTK")  
    sys.exit(1)
    
class GestionTablaClientes:
    """ Clase para la gestion de los clientes """
    
    def __init__(self,db,builder,con):
        #Objeto para acceder a los metodos
        self.db = db
        self.builder = builder
        self.con = con
        
    def on_clientes_destroy(self, widget, *signals):
        print("Cierro clientes con X y hago commit BD")
        self.db.commit()
        self.builder.get_object('clientes').hide()
        return True
    
    def on_nuevoCliente_destroy(self, widget, *signals):
        print("Cierro nuevo cliente con X")
        self.builder.get_object('nuevoCliente').hide()
        return True
        
    def on_calNewCli_destroy(self, widget, *signals):
        print("Cierro calendario fecha nacimiento cli con X")
        self.builder.get_object('calNewCli').hide()
        return True
    
    # A main (cerrar)
    def on_aMainDesdeCli_clicked(self,widget):
        print("Cierro clientes, hago commit en Bd y vuelvo a main")
        self.db.commit()
        self.builder.get_object('clientes').hide()
    
    #Nuevo cliente
    def on_add_cli_clicked(self,widget):
        print("A nuevo cliente")
        ventanaNuevoCliente = self.builder.get_object('nuevoCliente')
        ventanaNuevoCliente.show()
        self.builder.get_object('SaveNewCli').set_sensitive(True)
        self.builder.get_object('ModNewCli').set_sensitive(False)
        self.builder.get_object('label1_titulo_newcli1').set_text('NUEVO CLIENTE')
        nombre = self.builder.get_object("entry1AddNom").set_text('')
        apellidos = self.builder.get_object("entry2AddApe").set_text('')
        dni = self.builder.get_object("entry1AddDni").set_text('')
        pasaporte = self.builder.get_object("entry2AddPassport").set_text('')
        telefono = self.builder.get_object("entry1AddTel").set_text('')
        email = self.builder.get_object("entry1AddEmail").set_text('')
        fechaNacimiento = self.builder.get_object("entry1AddFNac").set_text('')
        direccion = self.builder.get_object("entry1AddDirecion").set_text('')
        id = self.builder.get_object("entry2AddIdCli").set_text('')
        #Oculto entry ID
        self.builder.get_object('entry2AddIdCli').set_visible(False)
        
    def on_cogeFechaNewCli_clicked(self,widget):
        print("Abro calendario para fecha de nacimiento nuevo cliente")
        self.builder.get_object('calNewCli').show()
    
    def on_cogeNewFechaNacCli_clicked(self,widget):
        print("Recojo la fecha de nacimiento del nuevo cliente")
        ano, mes, dia = self.builder.get_object('calendarNewCli').get_date()
        mes = mes + 1
        dia_text = "%s" %dia
        mes_text = "%s" %mes
        ano_text = "%s" %ano
        fechaFormateada = dia_text+"-"+mes_text+"-"+ano_text
        print("Fecha nacimiento formateada cliente: "+fechaFormateada)
        #pongo la fecha en el edittext de nueva venta y oculto ventana
        self.builder.get_object('entry1AddFNac').set_text(fechaFormateada)
        self.builder.get_object('calNewCli').hide()
        self.builder.get_object('nuevoCliente').show()
    
    def on_CancelNewCli_clicked(self,widteg):
        print("Cancelo nuevo cliente")
        btnCancelar = self.builder.get_object('nuevoCliente')
        btnCancelar.hide()
    
    def on_SaveNewCli_clicked(self,widget):
        print("Voy a guardar el nuevo cliente")
        nombre = self.builder.get_object("entry1AddNom").get_text()
        apellidos = self.builder.get_object("entry2AddApe").get_text()
        dni = self.builder.get_object("entry1AddDni").get_text()
        pasaporte = self.builder.get_object("entry2AddPassport").get_text()
        telefono = self.builder.get_object("entry1AddTel").get_text()
        email = self.builder.get_object("entry1AddEmail").get_text()
        fechaNacimiento = self.builder.get_object("entry1AddFNac").get_text()
        direccion = self.builder.get_object("entry1AddDirecion").get_text()
        print("Datos a insertar de cliente: ")
        print("Nombre: "+nombre)
        print("Apellidos:"+apellidos)
        print("Dni: "+dni)
        print("Pasaporte: "+pasaporte)
        print("Teléfono: "+telefono)
        print("Email: "+email)
        print("Fecha: "+fechaNacimiento)
        print("Direccion: "+direccion)
        
        
        
        #Transformo a UNICODE con UTF-8
        nombre = unicode(nombre, "utf-8")
        apellidos = unicode(apellidos, "utf-8")
        email = unicode(email, "utf-8")
        direccion = unicode(direccion, "utf-8")
        
        # Ahora voy a comprobar los campos si están correctos el tipo
        ventanaError = self.builder.get_object("ventanaError")
        
        error=0
        print(error)
        
        # Si algun campo lo dejo vacio
        if not(nombre) or not(apellidos) or not(dni) or not(pasaporte) or not(telefono) or not(email) or not(fechaNacimiento) or not(direccion):
            print("Muestro error por CAMPO VACIO de cliente")
            ventanaError.format_secondary_text("Dejaste algún campo vacío")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
        
        if fechaNacimiento == "dd/mm/aaaa":
            print("Muestro error por fecha no seleccionada de cliente")
            ventanaError.format_secondary_text("Debes seleccionar una fecha de nacimiento")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
        
        try:
            print("pruebo a convertir")
            numerico = int(telefono)
        except:
            print("Muestro error por fecha no seleccionada de cliente")
            ventanaError.format_secondary_text("El teléfono no es un número")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
        
        
        
        #CONSULTA UPDATE: self.db.execute("UPDATE Cliente (nombre,apellidos,fechaNacimiento,dni,pasaporte,telefono,email,direccion) VALUES (?,?,?,?,?,?,?,?) WHERE clienteID ='"+idCli+"'",(nombre,apellidos,dni,pasaporte,telefono,email,fechaNacimiento,direccion))
        #print("valor de var error fuera de if -> "+error)
        # Si no se ha producido algun error entonces intento guardar registro en BD
        if error==0:
            try:
                self.db.execute("INSERT INTO Cliente (nombre,apellidos,fechaNacimiento,dni,pasaporte,telefono,email,direccion) VALUES (?,?,?,?,?,?,?,?)",(nombre,apellidos,fechaNacimiento,dni,pasaporte,telefono,email,direccion))
            except(sqlite3.ProgrammingError, ValueError, TypeError) as tipoError:
                ventanaError.format_secondary_text(tipoError)
                ventanaError.run()
                ventanaError.hide()
            else:
                print("Cliente guardado correctamente :)")
                ventanaOk = self.builder.get_object("exitoAviso")
                ventanaOk.format_secondary_text("Cliente guardado correctamente")
                ventanaOk.run()
                ventanaOk.hide()
                
                #Vuelvo a cargar la lista de clientes
                self.lista_clientes("","liststore7","")
                self.builder.get_object('nuevoCliente').hide()
           
                
    #Activo botón modificar y eliminar si pulso en el listado
    def on_treeview1_cursor_changed(self,widget):
        print('Activo botonoes MODIFICAR y ELIMINAR CLIENTE con CLICK')
        self.builder.get_object('mod_cli').set_sensitive(True)
        self.builder.get_object('del_cli').set_sensitive(True)
        
    # Si hago doble click en client del listado abro modificar
    def on_treeview1_row_activated(self,widget,tipo,treeview):
        print("Abro MODIFICAR CLIENTE con DOBLE CLICK")
        print("A modificar cliente seleccionado en listado")
        seleccion = self.builder.get_object("treeview1").get_selection()
        print(type(seleccion))
        if seleccion == False:
            print("NO HAS SELECCIONADO NADA")
        #Ahora cojo modelo de liststore y ruta
        (modelo, pathlist) = seleccion.get_selected_rows()
        for path in pathlist:
            tree_iter = modelo.get_iter(path) #puntero a la fila
            idCli = modelo.get_value(tree_iter,8)
            print(idCli)
        
        #Muestro ventana de nuevo vliente con los datos rellenos
        self.builder.get_object('nuevoCliente').show()
        #cambio el titulo de la ventana
        self.builder.get_object('label1_titulo_newcli1').set_text('MODIFICAR CLIENTE')
        #Desactivo boton guardar un activo modificar
        self.builder.get_object('SaveNewCli').set_sensitive(False)
        self.builder.get_object('ModNewCli').set_sensitive(True)
        #realizo la busqueda de datos del cliente seleccionado
        buscaCliente = self.db.execute("SELECT * FROM Cliente WHERE clienteID = '"+idCli+"'")
        for row in buscaCliente:
            print("ROWS DATOS")
            print(row[0])
            print(row[1])
            print(row[2])
            print(row[3])
            print(row[4])
            print(row[5])
            print(row[6])
            print(row[7])
            print(row[8])
            #cojo los cuadros de texto y pongo los datos
            self.builder.get_object('entry1AddNom').set_text(row[1])
            self.builder.get_object('entry2AddApe').set_text(row[2])
            self.builder.get_object("entry1AddDni").set_text(row[3])
            self.builder.get_object("entry2AddPassport").set_text(row[4])
            self.builder.get_object("entry1AddTel").set_text(row[5])
            self.builder.get_object("entry1AddEmail").set_text(row[6])
            self.builder.get_object("entry1AddFNac").set_text(row[7])
            self.builder.get_object("entry1AddDirecion").set_text(row[8])
            self.builder.get_object("entry2AddIdCli").set_text(idCli)

    #Modifica un cliente PONE DATOS EN FORMULARIO
    def on_mod_cli_clicked(self,widget):
        print("A modificar cliente seleccionado en listado")
        seleccion = self.builder.get_object("treeview1").get_selection()
        print(type(seleccion))
        if seleccion == False:
            print("NO HAS SELECCIONADO NADA")
        #Ahora cojo modelo de liststore y ruta
        (modelo, pathlist) = seleccion.get_selected_rows()
        for path in pathlist:
            tree_iter = modelo.get_iter(path) #puntero a la fila
            idCli = modelo.get_value(tree_iter,8)
            print(idCli)
        
        #Muestro ventana de nuevo vliente con los datos rellenos
        self.builder.get_object('nuevoCliente').show()
        #cambio el titulo de la ventana
        self.builder.get_object('label1_titulo_newcli1').set_text('MODIFICAR CLIENTE')
        #Desactivo boton guardar un activo modificar
        self.builder.get_object('SaveNewCli').set_sensitive(False)
        self.builder.get_object('ModNewCli').set_sensitive(True)
        #realizo la busqueda de datos del cliente seleccionado
        buscaCliente = self.db.execute("SELECT * FROM Cliente WHERE clienteID = '"+idCli+"'")
        for row in buscaCliente:
            print("ROWS DATOS")
            print(row[0])
            print(row[1])
            print(row[2])
            print(row[3])
            print(row[4])
            print(row[5])
            print(row[6])
            print(row[7])
            print(row[8])
            #cojo los cuadros de texto y pongo los datos
            self.builder.get_object('entry1AddNom').set_text(row[1])
            self.builder.get_object('entry2AddApe').set_text(row[2])
            self.builder.get_object("entry1AddDni").set_text(row[3])
            self.builder.get_object("entry2AddPassport").set_text(row[4])
            self.builder.get_object("entry1AddTel").set_text(row[5])
            self.builder.get_object("entry1AddEmail").set_text(row[6])
            self.builder.get_object("entry1AddFNac").set_text(row[7])
            self.builder.get_object("entry1AddDirecion").set_text(row[8])
            self.builder.get_object("entry2AddIdCli").set_text(idCli)
    
    #Modifica cliente AL PULSAR EL BOTON
    def on_ModNewCli_clicked(self,widget):
        print('Pulso en boton modificar cliente del formulario')
        nombre = self.builder.get_object("entry1AddNom").get_text()
        apellidos = self.builder.get_object("entry2AddApe").get_text()
        dni = self.builder.get_object("entry1AddDni").get_text()
        pasaporte = self.builder.get_object("entry2AddPassport").get_text()
        telefono = self.builder.get_object("entry1AddTel").get_text()
        email = self.builder.get_object("entry1AddEmail").get_text()
        fechaNacimiento = self.builder.get_object("entry1AddFNac").get_text()
        direccion = self.builder.get_object("entry1AddDirecion").get_text()
        idCliente = self.builder.get_object('entry2AddIdCli').get_text()
        print("El ID del cliente a modificar es: "+idCliente)
        
        #Transformo a UNICODE con UTF-8
        nombre = unicode(nombre, "utf-8")
        apellidos = unicode(apellidos, "utf-8")
        email = unicode(email, "utf-8")
        direccion = unicode(direccion, "utf-8")
        
        # Ahora voy a comprobar los campos si están correctos el tipo
        ventanaError = self.builder.get_object("ventanaError")
        
        error=0
        print(error)
        
        # Si algun campo lo dejo vacio
        if not(nombre) or not(apellidos) or not(dni) or not(pasaporte) or not(telefono) or not(email) or not(fechaNacimiento) or not(direccion):
            print("Muestro error por CAMPO VACIO de cliente MODFICADO")
            ventanaError.format_secondary_text("Dejaste algún campo vacío al modificar los datos")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
        
        #compruebo que el telefono se valor numerico
        try:
            print("pruebo a convertir")
            numerico = int(telefono)
        except:
            print("Muestro error por fecha no seleccionada de cliente")
            ventanaError.format_secondary_text("El teléfono no es un número")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
        
        #CONSULTA UPDATE: 
        #print("valor de var error fuera de if -> "+error)
        # Si no se ha producido algun error entonces intento guardar registro en BD
        if error==0:
            try:
                self.db.execute("UPDATE Cliente SET nombre = ?, apellidos = ?, fechaNacimiento = ?, dni = ?, pasaporte = ?, telefono = ?, email = ?, direccion = ? WHERE clienteID ='"+idCliente+"'",(nombre,apellidos,dni,pasaporte,telefono,email,fechaNacimiento,direccion))
            except(sqlite3.ProgrammingError, ValueError, TypeError) as tipoError:
                ventanaError.format_secondary_text(tipoError)
                ventanaError.run()
                ventanaError.hide()
            else:
                print("Cliente guardado correctamente :)")
                ventanaOk = self.builder.get_object("exitoAviso")
                ventanaOk.format_secondary_text("Se han modificado los datos del cliente correctamente")
                ventanaOk.run()
                ventanaOk.hide()
                
                #Vuelvo a cargar la lista de clientes
                self.builder.get_object('cli_busca_cli').set_sensitive(False)
                self.builder.get_object('mod_cli').set_sensitive(False)
                self.builder.get_object('del_cli').set_sensitive(False)
                self.builder.get_object('entry_busq_cli').set_text('')
                self.builder.get_object('comboboxClientes').set_active(-1)
                self.lista_clientes("","liststore7","")
                self.builder.get_object('nuevoCliente').hide()
        
    #Activacion de boton buscar en clientes
    def on_comboboxClientes_changed(self,widget):
        print("Activo el boton para buscar cliente")
        self.builder.get_object('cli_busca_cli').set_sensitive(True)
    #Buscar un cliente
    def on_cli_busca_cli_clicked(self,widget):
        print("Hago busqueda de cliente")
        comboSeleccionado = self.builder.get_object('comboboxClientes').get_active_text()
        textoBusqueda = self.builder.get_object('entry_busq_cli').get_text()
        print("Busca: "+textoBusqueda+" en campo "+comboSeleccionado)
        self.lista_clientes(comboSeleccionado,"liststore7",textoBusqueda)
        self.builder.get_object('cli_busca_cli').set_sensitive(False)
        self.builder.get_object('mod_cli').set_sensitive(False)
        self.builder.get_object('del_cli').set_sensitive(False)
        self.builder.get_object('entry_busq_cli').set_text('')
        self.builder.get_object('comboboxClientes').set_active(-1)
    
    #Eliminar un cliente
    def on_del_cli_clicked(self,widget):
        print("Voy a eliminar el cliente seleccionado en listado")
        #Cojo el handler de la fila seleccionada
        seleccion = self.builder.get_object("treeview1").get_selection()
        print(type(seleccion))
        #Ahora cojo modelo de liststore y ruta
        (modelo, pathlist) = seleccion.get_selected_rows()
        for path in pathlist:
            tree_iter = modelo.get_iter(path) #puntero a la fila
            idCli = modelo.get_value(tree_iter,8)
            print(idCli)
        #Muestro mensaje para confirmar borrado de cliente
        ventanaConfirmar = self.builder.get_object("confirmar")
        ventanaConfirmar.format_secondary_text("¿Desea borrar el cliente seleccionado?")
        respuesta=ventanaConfirmar.run()
        #respuestaSerá -5 si le hemos dado a Aceptar, será -6 si Cancelar
        ventanaConfirmar.hide()

        if respuesta==-5:
            print("Entro a BORRAR CLIENTE")
            self.db.execute("DELETE FROM Cliente where clienteID="+str(idCli))
                
            #Llamo a la ventana de exito al borrar cliente
            ventanaOk = self.builder.get_object("exitoAviso")
            ventanaOk.format_secondary_text("Cliente borrado correctamente")
            ventanaOk.run()
            ventanaOk.hide()
            
            self.builder.get_object('cli_busca_cli').set_sensitive(False)
            self.builder.get_object('mod_cli').set_sensitive(False)
            self.builder.get_object('del_cli').set_sensitive(False)
            self.builder.get_object('entry_busq_cli').set_text('')
            self.builder.get_object('comboboxClientes').set_active(-1)
            #Actualizo todos los listore
            self.lista_clientes("","liststore7","")
        
        
    # funcion para inicializar los treeview de clientes <--- PASO 1 --->
    def inicializa_listado(self,treeview):
        """Inicializa los CellRenderer de un treeview pasado como parámetro. Esto siempre se hará igual para cada TreeView"""
        celda = gtk.CellRendererText()
        columnas=self.builder.get_object(treeview).get_columns()
        i=0
        for col_i in columnas:
            col_i.pack_start(celda)
            col_i.add_attribute(celda,"text", i)
            i=i+1
        print("exito inicializando treeview clisente")
    
    # funcion que lista datos de bd en treeview de clientes
    # también lista las búsquedas
    def lista_clientes(self,tipo,lista,filtro):
            """Lista clientes. Si tipo es "" lo listo todo, si no, lo hace por tipo """
            self.lista=self.builder.get_object(lista)
            self.lista.clear()#Limpia la lista
            busqueda = ""
            if tipo == "":
                print("Llego a buscar clientes en BD")
                busqueda = self.db.execute('SELECT * FROM Cliente')
            else:
                busqueda = self.db.execute("SELECT * FROM Cliente WHERE " + tipo + " LIKE '%"+filtro+"%'")
            
            for row in busqueda: 
                #Empieza por la [1] porque el ID es la [0]
                self.lista.append([row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[0]])
                print("Listo clientes en tabla")
            
                
    #menu emergente sobre el listado (treeview)
    def on_treeview1_button_press_event(self,treeview,evento):
        print("Evento press en la lista en clientes")
        pulsado = evento.button
        # si pulsa boton derecho
        if pulsado == 3:
            print("has pulsado con el boton derecho del raton")
            #creo menu
            self.menu = gtk.Menu()
            #creo boton modificar
            menu_modificar = gtk.ImageMenuItem(gtk.STOCK_EDIT)
            self.menu.append(menu_modificar)
            menu_modificar.connect("activate", self.on_mod_cli_clicked)
            #creo boton borrar
            menu_borrar = gtk.ImageMenuItem(gtk.STOCK_DELETE)
            self.menu.append(menu_borrar)
            menu_borrar.connect("activate", self.on_del_cli_clicked)
            #muestro
            self.menu.popup(None,None,None,evento.button,evento.time)
            menu_modificar.show()
            menu_borrar.show()
            
    