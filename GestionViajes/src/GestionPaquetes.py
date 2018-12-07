# -*- coding: utf-8 -*-


"""
    Gestion de paquetes para agencia de viajes
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
    
class GestionTablaPaquetes:
    """ Clase para la gestion de los paquetes """
    
    def __init__(self,db,builder,con):
        #Objeto para acceder a los metodos
        self.db = db
        self.builder = builder
        self.con = con
        
    def on_destroy(self, widget, *signals):
        print("Cerrando base de datos")
        self.db.commit()
        self.db.close()           
        gtk.main_quit()
    
    #Cerrar con la CRUZ
    def on_paquetes_destroy(self, widget, *signals):
        print("Cierro paquetes con X y hago commit BD")
        self.db.commit()
        self.builder.get_object('paquetes').hide()
        return True
        
    def on_nuevoPaquete_destroy(self,widget,*signals):
        print("Cierrro ventana nuevo paquet con X")
        self.builder.get_object('nuevoPaquete').hide()
        return True
    
    #Cerrar y volver a main
    def on_aMainDesdePaq_clicked(self,widget):
        print('Cierro paquetes, hago commit en BD y vuelvo al main')
        self.db.commit()
        self.builder.get_object('paquetes').hide()
        
        
    #Nuevo paquete
    def on_button_add_paq_clicked(self,widget):
        print("A nuevo paquete")
        ventanaNuevoPaquete = self.builder.get_object("nuevoPaquete")
        ventanaNuevoPaquete.show()
        self.builder.get_object('label1_titulo_newPaq').set_text('NUEVO PAQUETE')
        self.builder.get_object('buttonModPaqForm').set_sensitive(False)
        self.builder.get_object('button4SaveNewCli1').set_sensitive(True)
        nombre = self.builder.get_object("entry1AddNomPaq").set_text('')
        precio = self.builder.get_object("entry2precioPaq").set_text('')
        destino = self.builder.get_object("entry1Destino").set_text('')
        duracion = self.builder.get_object("entry1AddDurPaq").set_text('')
        hospedaje = self.builder.get_object("entry1hostPaq").set_text('')
        transporte = self.builder.get_object("entry1medtrans").set_text('')
        id = self.builder.get_object('entryAddIdPaq').set_text('')
        #oculto el entry de id
        self.builder.get_object('entryAddIdPaq').set_visible(False)
    
    #Cancelo el nuevo paquete
    def on_button4CancelNewCli1_clicked(self,widget):
        print("Cancelo el nuevo paquete")
        vuelvoPaquetes = self.builder.get_object("nuevoPaquete")
        vuelvoPaquetes.hide()
    
    #Guardo el nuevo paquete
    def on_button4SaveNewCli1_clicked(self,widget):
        print("Voy a guardar el nuevo paquete")
        nombre = self.builder.get_object("entry1AddNomPaq").get_text()
        precio = self.builder.get_object("entry2precioPaq").get_text()
        destino = self.builder.get_object("entry1Destino").get_text()
        duracion = self.builder.get_object("entry1AddDurPaq").get_text()
        hospedaje = self.builder.get_object("entry1hostPaq").get_text()
        transporte = self.builder.get_object("entry1medtrans").get_text()
        print("Datos paquete a insertar: ")
        print("Nombre: "+nombre)
        print("Precio:"+precio)
        print("Destino: "+destino)
        print("Duración: "+duracion)
        print("Transporte: "+transporte)
        print("Hospedaje: "+hospedaje)
        
        #Transformo a UNICODE con UTF-8
        nombre = unicode(nombre, "utf-8")
        destino = unicode(destino, "utf-8")
        duracion = unicode(duracion, "utf-8")
        transporte = unicode(transporte, "utf-8")
        hospedaje = unicode(hospedaje, "utf-8")
        
        # Ahora voy a comprobar los campos si están correctos el tipo
        ventanaError = self.builder.get_object("ventanaError")
        
        error=0
        print(error)
        
        # Si algun campo lo dejo vacio
        if not(nombre) or not(precio) or not(destino) or not(duracion) or not(transporte) or not(hospedaje):
            print("Muestro error por CAMPO VACIO en paquetes")
            ventanaError.format_secondary_text("Dejaste algún campo vacío")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
        
        #compruebo que el telefono se valor numerico
        try:
            print("pruebo a convertir")
            numerico = int(precio)
        except:
            print("Muestro error por precio de paquete")
            ventanaError.format_secondary_text("El precio no es un número")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
        
        #print("valor de var error fuera de if -> "+error)
        # Si no se ha producido algun error entonces intento guardar registro en BD
        if error==0:
            try:
                self.db.execute("INSERT INTO Paquete (nombre,precio,destino,duracion,transporte,hospedaje) VALUES (?,?,?,?,?,?)",(nombre,precio,destino,duracion,transporte,hospedaje))
            except(sqlite3.ProgrammingError, ValueError, TypeError) as tipoError:
                ventanaError.format_secondary_text(tipoError)
                ventanaError.run()
                ventanaError.hide()
            else:
                print("Paquete guardado correctamente :)")
                ventanaOk = self.builder.get_object("exitoAviso")
                ventanaOk.format_secondary_text("Paquete guardado correctamente")
                ventanaOk.run()
                ventanaOk.hide()
                
                #Vuelvo a cargar la lista de paquetes
                self.lista_paquetes("","liststore2","")#listado de paquete principal
                self.builder.get_object("nuevoPaquete").hide()
                self.builder.get_object("paquetes").show()
    
    # Activo botonoes de MOD y DEL PAQUETES
    def on_treeview2Paq_row_activated(self,widget,tipo,treeview):
        print("Con doble click abro modificar del paquete seleccionado")
        seleccion = self.builder.get_object("treeview2Paq").get_selection()
        print(type(seleccion))
        #Ahora cojo modelo de liststore y ruta
        (modelo, pathlist) = seleccion.get_selected_rows()
        for path in pathlist:
            tree_iter = modelo.get_iter(path) #puntero a la fila
            idPaquete = modelo.get_value(tree_iter,6)
            print(idPaquete)
        #Muestro ventana de nuevo vliente con los datos rellenos
        self.builder.get_object('nuevoPaquete').show()
        #cambio el titulo de la ventana
        self.builder.get_object('label1_titulo_newPaq').set_text('MODIFICAR PAQUETE')
        #Desactivo boton guardar un activo modificar
        self.builder.get_object('buttonModPaqForm').set_sensitive(True)
        self.builder.get_object('button4SaveNewCli1').set_sensitive(False)
        #realizo la busqueda de datos del paquete seleccionado
        buscaPaquete = self.db.execute("SELECT * FROM Paquete WHERE paqueteID = '"+idPaquete+"'")
        for row in buscaPaquete:
            print(row)
            #cojo los cuadros de texto y pongo los datos
            self.builder.get_object("entry1AddNomPaq").set_text(str(row[1]))
            self.builder.get_object("entry2precioPaq").set_text(str(row[2]))
            self.builder.get_object("entry1Destino").set_text(str(row[5]))
            self.builder.get_object("entry1AddDurPaq").set_text(str(row[4]))
            self.builder.get_object("entry1hostPaq").set_text(str(row[3]))
            self.builder.get_object("entry1medtrans").set_text(str(row[6]))
            self.builder.get_object('entryAddIdPaq').set_text(idPaquete)
        
    # Si hago clic selecciono el paquete y activo botones MOD y DEL
    def on_treeview2Paq_cursor_changed(self,widget):
        print("Activo botones MODIFICAR Y BORRAR PAQUETE")
        self.builder.get_object('button_mod_paq').set_sensitive(True)
        self.builder.get_object('button_del_paq').set_sensitive(True)
    
    #Modifico un paquete seleccionado PONE DATOS EN FORM DESDE LISTADO SELECCIONADO
    def on_button_mod_paq_clicked(self,widget):
        print("Modifico un paquete seleccionado de la lista")
        seleccion = self.builder.get_object("treeview2Paq").get_selection()
        print(type(seleccion))
        #Ahora cojo modelo de liststore y ruta
        (modelo, pathlist) = seleccion.get_selected_rows()
        for path in pathlist:
            tree_iter = modelo.get_iter(path) #puntero a la fila
            idPaquete = modelo.get_value(tree_iter,6)
            print(idPaquete)
        #Muestro ventana de nuevo vliente con los datos rellenos
        self.builder.get_object('nuevoPaquete').show()
        #cambio el titulo de la ventana
        self.builder.get_object('label1_titulo_newPaq').set_text('MODIFICAR PAQUETE')
        #Desactivo boton guardar un activo modificar
        self.builder.get_object('buttonModPaqForm').set_sensitive(True)
        self.builder.get_object('button4SaveNewCli1').set_sensitive(False)
        #realizo la busqueda de datos del paquete seleccionado
        buscaPaquete = self.db.execute("SELECT * FROM Paquete WHERE paqueteID = '"+idPaquete+"'")
        for row in buscaPaquete:
            print(row)
            #cojo los cuadros de texto y pongo los datos
            self.builder.get_object("entry1AddNomPaq").set_text(str(row[1]))
            self.builder.get_object("entry2precioPaq").set_text(str(row[2]))
            self.builder.get_object("entry1Destino").set_text(str(row[5]))
            self.builder.get_object("entry1AddDurPaq").set_text(str(row[4]))
            self.builder.get_object("entry1hostPaq").set_text(str(row[3]))
            self.builder.get_object("entry1medtrans").set_text(str(row[6]))
            self.builder.get_object('entryAddIdPaq').set_text(idPaquete)
        
    #Modificar paquete DESDE BOTON MODIFICAR DEL FORMULARIO
    def on_buttonModPaqForm_clicked(self,widget):
        print("Pulso en btn modificar paquete en formulario")
        nombre = self.builder.get_object("entry1AddNomPaq").get_text()
        precio = self.builder.get_object("entry2precioPaq").get_text()
        destino = self.builder.get_object("entry1Destino").get_text()
        duracion = self.builder.get_object("entry1AddDurPaq").get_text()
        hospedaje = self.builder.get_object("entry1hostPaq").get_text()
        transporte = self.builder.get_object("entry1medtrans").get_text()
        idPaquete = self.builder.get_object('entryAddIdPaq').get_text()
        print("El ID del paquete a modificar es: "+idPaquete)
        
        #Transformo a UNICODE con UTF-8
        nombre = unicode(nombre, "utf-8")
        destino = unicode(destino, "utf-8")
        duracion = unicode(duracion, "utf-8")
        transporte = unicode(transporte, "utf-8")
        hospedaje = unicode(hospedaje, "utf-8")
        
        # Ahora voy a comprobar los campos si están correctos el tipo
        ventanaError = self.builder.get_object("ventanaError")
        
        error=0
        print(error)
        
        # Si algun campo lo dejo vacio
        if not(nombre) or not(precio) or not(destino) or not(duracion) or not(hospedaje) or not(transporte) or not(idPaquete):
            print("Muestro error por CAMPO VACIO de paquete MODFICADO")
            ventanaError.format_secondary_text("Dejaste algún campo vacío al modificar los datos")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
        
        #compruebo que el telefono se valor numerico
        try:
            print("pruebo a convertir")
            numerico = int(precio)
        except:
            print("Muestro error por precio no numero modifica paquete")
            ventanaError.format_secondary_text("El precio no es un número")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
        
        #CONSULTA UPDATE: 
        #print("valor de var error fuera de if -> "+error)
        # Si no se ha producido algun error entonces intento guardar registro en BD
        if error==0:
            try:
                self.db.execute("UPDATE Paquete SET nombre = ?, precio = ?, destino = ?, duracion = ?, hospedaje = ?, transporte = ? WHERE paqueteID ='"+idPaquete+"'",(nombre,precio,destino,duracion,hospedaje,transporte))
            except(sqlite3.ProgrammingError, ValueError, TypeError) as tipoError:
                ventanaError.format_secondary_text(tipoError)
                ventanaError.run()
                ventanaError.hide()
            else:
                print("paquete modificado correctamente :)")
                ventanaOk = self.builder.get_object("exitoAviso")
                ventanaOk.format_secondary_text("Se han modificado los datos del paquete correctamente")
                ventanaOk.run()
                ventanaOk.hide()
                
                #Vuelvo a cargar la lista de clientes
                self.lista_paquetes("","liststore2","")#listado de paquete principal
                self.builder.get_object('nuevoPaquete').hide()

    #Búsqueda de un paquete
    def on_paq_busca_pa_clicked(self,widget):
        print("Hago búsqueda de un paquete")
        comboSeleccionado = self.builder.get_object('comboboxPaquetes').get_active_text()
        textoBusqueda = self.builder.get_object('entry1_busqPaq').get_text()
        print("Busca: "+textoBusqueda+" en campo "+comboSeleccionado)
        self.lista_paquetes(comboSeleccionado,"liststore2",textoBusqueda)
    
    #Elimino un paquete
    def on_button_del_paq_clicked(self,widget):
        #Cojo el handler de la fila seleccionada
        seleccion = self.builder.get_object("treeview2Paq").get_selection()
        print(type(seleccion))
        #Ahora cojo modelo de liststore y ruta
        (modelo, pathlist) = seleccion.get_selected_rows()
        for path in pathlist:
            tree_iter = modelo.get_iter(path) #puntero a la fila
            idPaquete = modelo.get_value(tree_iter,6)
            print(idPaquete)
        
        #Muestro mensaje para confirmar borrado de cliente
        ventanaConfirmar = self.builder.get_object("confirmar")
        ventanaConfirmar.format_secondary_text("¿Desea borrar el paquete seleccionado?")
        respuesta=ventanaConfirmar.run()
        #respuestaSerá -5 si le hemos dado a Aceptar, será -6 si Cancelar
        ventanaConfirmar.hide()

        if respuesta==-5:
            print("Entro a BORRAR PAQUETE")
            self.db.execute("DELETE FROM Paquete where paqueteID="+idPaquete)
                
            #Llamo a la ventana de exito al borrar cliente
            ventanaOk = self.builder.get_object("exitoAviso")
            ventanaOk.format_secondary_text("Paquete borrado correctamente")
            ventanaOk.run()
            ventanaOk.hide()

            #Actualizo todos los listore
            self.lista_paquetes("","liststore2","")
    # funcion para inicializar el treeview de paquetes <--- PASO 1 --->
    def inicializa_listado(self,treeview):
        """Inicializa los CellRenderer de un treeview pasado como parámetro. Esto siempre se hará igual para cada TreeView"""
        celda = gtk.CellRendererText()
        columnas=self.builder.get_object(treeview).get_columns()
        i=0
        for col_i in columnas:
            col_i.pack_start(celda)
            col_i.add_attribute(celda,"text", i)
            i=i+1
        print("exito inicializando treeview paquetes")
    
    # funcion que lista datos de bd en treeview de paquetes
    # también lista las búsquedas
    def lista_paquetes(self,tipo,lista,filtro):
            """Lista paquetes. Si tipo es "" lo listo todo, si no, lo hace por tipo """
            self.lista=self.builder.get_object(lista)
            self.lista.clear()#Limpia la lista
            busqueda = ""

            if tipo=="":
                print("Llego a buscar paquetes en BD")
                busqueda=self.db.execute('SELECT * FROM Paquete')
            else:
                print("Busco paquete por tipo "+tipo)
                busqueda = self.db.execute("SELECT * FROM Paquete WHERE " + tipo + " LIKE '%"+filtro+"%'")

            for row in busqueda: 
                print(lista)
                #Empieza por la [1] porque el ID es la [0]
                self.lista.append([row[1],row[2],row[5],row[4],row[3],row[6],row[0]])
                print("Listo paquetes en tabla")
    
    def on_comboboxPaquetes_changed(self,widget):
        print("activo boton buscar en paquetes")
        self.builder.get_object('paq_busca_pa').set_sensitive(True)
    
    #menu emergente en listado (treeview)
    def on_treeview2Paq_button_press_event(self,treeview,evento):
        print("Evento press en la lista en paquetes")
        pulsado = evento.button
        # si pulsa boton derecho
        if pulsado == 3:
            print("has pulsado con el boton derecho del raton")
            #creo menu
            self.menu = gtk.Menu()
            #creo boton modificar
            menu_modificar = gtk.ImageMenuItem(gtk.STOCK_EDIT)
            self.menu.append(menu_modificar)
            menu_modificar.connect("activate", self.on_button_mod_paq_clicked)
            #creo boton borrar
            menu_borrar = gtk.ImageMenuItem(gtk.STOCK_DELETE)
            self.menu.append(menu_borrar)
            menu_borrar.connect("activate", self.on_button_del_paq_clicked)
            #muestro
            self.menu.popup(None,None,None,evento.button,evento.time)
            menu_modificar.show()
            menu_borrar.show()