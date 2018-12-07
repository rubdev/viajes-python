# -*- coding: utf-8 -*-


"""
    Gestion de ventas para agencia de viajes
"""


#Importamos las clases sys, pygtk, gtk y gtk.glade
import sys
import time

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
    
class GestionTablaVentas:
    """ Clase para la gestion de las ventas """
    
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
    
    #Cerrar con la cruz
    def on_ventas_destroy(self, widget, *signals):
        print("Cierro ventas con X y hago commit BD")
        self.db.commit()
        self.builder.get_object('ventas').hide()
        return True

    def on_nuevaVenta_destroy(self, widget, *signals):
        print("Cierro ventana nueva venta con X")
        self.builder.get_object('nuevaVenta').hide()
        return True
    
    def on_buscaClienteVenta_destroy(self,widget,*signals):
        print("Cierrro busq cliente venta con X")
        self.builder.get_object('buscaClienteVenta').hide()
        return True
    
    def on_buscaPaqueteVenta_destroy(self,widget,*signals):
        print("Cierro busq paq venta con X")
        self.builder.get_object('buscaPaqueteVenta').hide()
        return True
    
    def on_calendario_destroy(self,widget,*signals):
        print("Cierro fecha ini venta con X")
        self.builder.get_object('calendario').hide()
        return True
    
    def on_calendarioFinVenta_destroy(self,widget,*signals):
        print("Cierro fecha fin venta con X")
        self.builder.get_object('calendarioFinVenta').hide()
        return True
    
    #a menu principal
    def on_aMainDesdeVenta_clicked(self,widget):
        print('Hago commit BD y salgo al menu principal desde ventas')
        self.db.commit()
        self.builder.get_object('ventas').hide()
            
    #Para una NUEVA VENTA
    def on_button1_add_vent_clicked(self, widget):
        print("A nueva venta")
        ventanaNuevaVenta = self.builder.get_object("nuevaVenta")
        ventanaNuevaVenta.show()
        self.builder.get_object('label_nueva_venta').set_text("NUEVA VENTA")
        self.builder.get_object('modificaVentaBtn').set_sensitive(False)
        self.builder.get_object('guarda_new_venta').set_sensitive(True)
        self.builder.get_object("sel_cli_new_venta").set_text('')
        self.builder.get_object("sel_paq_new_venta").set_text('')
        self.builder.get_object("selec_fe_ini_new_venta").set_text('')
        self.builder.get_object("selec_fe_fin_new_venta").set_text('')
        self.builder.get_object('idVentaForm').set_text('')
        
        #Oculto id venta
        self.builder.get_object('idVentaForm').set_visible(False)
        self.builder.get_object('idFormClienteVenta').set_visible(False)
        self.builder.get_object('idFormPaquetesVenta').set_visible(False)
    
    def on_busq_cli_new_venta_clicked(self,widget):
        print("A buscar cliente para nueva venta")
        buscaClienteVenta = self.builder.get_object("buscaClienteVenta")
        buscaClienteVenta.show()
        self.lista_cliente_venta("","tabla_bus_cli_new_venta","")
        self.builder.get_object('comboboxSelCliVenta').set_active(-1)
        self.builder.get_object('term_busca_cli_new_venta').set_text('')
        self.builder.get_object('btn_busq_cli_new_venta').set_sensitive(False)
        self.builder.get_object('save_busc_cli_new_venta').set_sensitive(False)
        self.lista_cliente_venta('nombre',"tabla_bus_cli_new_venta",'')
        
    #Activo buscar despues de seleccionar combo busqueda de cliente
    def on_comboboxSelCliVenta_changed(self,widget):
        print("Activo boton buscar cliente para nueva venta EEEEEEEEEEEEEEEEE")
        self.builder.get_object('btn_busq_cli_new_venta').set_sensitive(True)
    
    def on_save_busc_cli_new_venta_clicked(self,widget):
        print("Selecciono cliente para la venta")
        #Cojo el handler de la fila seleccionada
        seleccion = self.builder.get_object("treeview3").get_selection()
        print(type(seleccion))
        #Ahora cojo modelo de liststore y ruta
        (modelo, pathlist) = seleccion.get_selected_rows()
        for path in pathlist:
            tree_iter = modelo.get_iter(path) #puntero a la fila
            idCliente = modelo.get_value(tree_iter,4)
            nombre = modelo.get_value(tree_iter,0)
            apellido = modelo.get_value(tree_iter,1)
            print(idCliente)
            print(nombre+" "+apellido)
        #Mando el id al gtkEntry de cliente para venta
        self.builder.get_object('sel_cli_new_venta').set_text(nombre+" "+apellido)
        self.builder.get_object('idFormClienteVenta').set_text(idCliente)
        #Oculto la ventana
        self.builder.get_object('buscaClienteVenta').hide()
        
    def on_treeview3_row_activated(self,widget,tipo,treeview):
        print("selecciono cliente venta con doble click")
        #Cojo el handler de la fila seleccionada
        seleccion = self.builder.get_object("treeview3").get_selection()
        print(type(seleccion))
        #Ahora cojo modelo de liststore y ruta
        (modelo, pathlist) = seleccion.get_selected_rows()
        for path in pathlist:
            tree_iter = modelo.get_iter(path) #puntero a la fila
            idCliente = modelo.get_value(tree_iter,4)
            nombre = modelo.get_value(tree_iter,0)
            apellido = modelo.get_value(tree_iter,1)
            print(idCliente)
            print(nombre+" "+apellido)
        #Mando el id al gtkEntry de cliente para venta
        self.builder.get_object('sel_cli_new_venta').set_text(nombre+" "+apellido)
        self.builder.get_object('idFormClienteVenta').set_text(idCliente)
        #Oculto la ventana
        self.builder.get_object('buscaClienteVenta').hide()
    
    def on_treeview2Vent_row_activated(self,widget):
        print("Selecciono cliente para la venta")
        #Cojo el handler de la fila seleccionada
        seleccion = self.builder.get_object("treeview3").get_selection()
        print(type(seleccion))
        #Ahora cojo modelo de liststore y ruta
        (modelo, pathlist) = seleccion.get_selected_rows()
        for path in pathlist:
            tree_iter = modelo.get_iter(path) #puntero a la fila
            idCliente = modelo.get_value(tree_iter,4)
            nombre = modelo.get_value(tree_iter,0)
            apellido = modelo.get_value(tree_iter,1)
            print(idCliente)
            print(nombre+" "+apellido)
        #Mando el id al gtkEntry de cliente para venta
        self.builder.get_object('sel_cli_new_venta').set_text(nombre+" "+apellido)
        self.builder.get_object('idFormClienteVenta').set_text(idCliente)
        #Oculto la ventana
        self.builder.get_object('buscaClienteVenta').hide()
    
    def on_cancel_busc_cli_new_venta_clicked(self,widget):
        print("Cancelo la seleccion del cliente para la venta")
        btnCancelar = self.builder.get_object('buscaClienteVenta')
        btnCancelar.hide()
    
    def on_save_busc_paq_new_venta1_clicked(self,widget):
        print("Selecciono paquete para la venta")
        #Cojo el handler de la fila seleccionada
        seleccion = self.builder.get_object("treeview2").get_selection()
        print(type(seleccion))
        #Ahora cojo modelo de liststore y ruta
        (modelo, pathlist) = seleccion.get_selected_rows()
        for path in pathlist:
            tree_iter = modelo.get_iter(path) #puntero a la fila
            idPaq = modelo.get_value(tree_iter,3)
            nombre = modelo.get_value(tree_iter,1)
            print(idPaq)
            print(nombre)
        #Mando el id al gtkEntry de paquete para venta
        self.builder.get_object('sel_paq_new_venta').set_text(nombre)
        self.builder.get_object('idFormPaquetesVenta').set_text(idPaq)
        #Oculto la ventana
        self.builder.get_object('buscaPaqueteVenta').hide()
            
            
    def on_treeview2_row_activated(self,widget,tipo,treeview):
        print("Selecciona paquete venta con dobleclick")
        print("Selecciono paquete para la venta")
        #Cojo el handler de la fila seleccionada
        seleccion = self.builder.get_object("treeview2").get_selection()
        print(type(seleccion))
        #Ahora cojo modelo de liststore y ruta
        (modelo, pathlist) = seleccion.get_selected_rows()
        for path in pathlist:
            tree_iter = modelo.get_iter(path) #puntero a la fila
            idPaq = modelo.get_value(tree_iter,3)
            nombre = modelo.get_value(tree_iter,1)
            print(idPaq)
            print(nombre)
            
        #Mando el id al gtkEntry de paquete para venta
        self.builder.get_object('sel_paq_new_venta').set_text(nombre)
        self.builder.get_object('idFormPaquetesVenta').set_text(idPaq)
        #Oculto la ventana
        self.builder.get_object('buscaPaqueteVenta').hide()
    
    def on_cancel_busc_paq_new_venta1_clicked(self,widget):
        print("Cancelo la seleccion de paquete para la venta")
        btnCancelar = self.builder.get_object("buscaPaqueteVenta")
        btnCancelar.hide()
        self.builder.get_object('term_busca_paq_new_venta1').set_text('')
        self.builder.get_object('btn_busq_paq_new_venta1').set_sensitive(False)
    
    def on_busq_paq_new_venta_clicked(self,widget):
        print("A buscar paquete para nueva venta")
        buscaPaqueteVenta = self.builder.get_object("buscaPaqueteVenta")
        buscaPaqueteVenta.show()
        self.lista_paquete_venta("","tabla_bus_paq_new_venta","")
        self.builder.get_object('comboboxSelPaqVenta1').set_active(-1)
        self.builder.get_object('term_busca_paq_new_venta1').set_text('')
        self.builder.get_object('btn_busq_paq_new_venta1').set_sensitive(False)
        self.builder.get_object('save_busc_paq_new_venta1').set_sensitive(False)
        self.lista_paquete_venta("nombre","tabla_bus_paq_new_venta","")
    
    #Activo boton buscar paquete en nueva venta seleccion paquete
    def on_comboboxSelPaqVenta1_changed(self,widget):
        print("Activo boton buscar paquete en nueva venta")
        self.builder.get_object('btn_busq_paq_new_venta1').set_sensitive(True)
        
    # Abre calendario para fecha INICIO de venta
    def on_abre_cal_ini_new_venta_clicked(self,widget):
        print("A seleccion fecha inicio venta")
        calendario = self.builder.get_object('calendario');
        calendario.show()
    
    # Selecciona y pone fecha de INICIO en venta
    def on_cogeFecha_clicked(self,widget):
        ano, mes, dia = self.builder.get_object('calendar').get_date()
        mes = mes + 1
        dia_text = "%s" %dia
        mes_text = "%s" %mes
        ano_text = "%s" %ano
        fechaFormateada = dia_text+"-"+mes_text+"-"+ano_text
        print("Fecha formateada inicio venta: "+fechaFormateada)
        #pongo la fecha en el edittext de nueva venta y oculto ventana
        self.builder.get_object('selec_fe_ini_new_venta').set_text(fechaFormateada)
        self.builder.get_object('calendario').hide()
        self.builder.get_object('nuevaVenta').show()
    
    # Abre calendario para fecha FIN de venta
    def on_abre_cal_fin_new_venta_clicked(self,widget):
        print("A seleccion fecha fin nueva venta")
        calendario = self.builder.get_object('calendarioFinVenta');
        calendario.show()
            
    # Selecciona y pone fecha de FIN en venta
    def on_cogeFechaFinVenta_clicked(self,widget):
        ano, mes, dia = self.builder.get_object('calendarFinVenta').get_date()
        mes = mes + 1
        dia_text = "%s" %dia
        mes_text = "%s" %mes
        ano_text = "%s" %ano
        fechaFormateada = dia_text+"-"+mes_text+"-"+ano_text
        print("Fecha formateada fin venta: "+fechaFormateada)
        #pongo la fecha en el edittext de nueva venta y oculto ventana
        self.builder.get_object('selec_fe_fin_new_venta').set_text(fechaFormateada)
        self.builder.get_object('calendarioFinVenta').hide()
        self.builder.get_object('nuevaVenta').show()

    #Guardo nueva venta
    def on_guarda_new_venta_clicked(self,widget):
        print("Guardo nueva venta")
        clienteID = self.builder.get_object("idFormClienteVenta").get_text()
        paqueteID = self.builder.get_object("idFormPaquetesVenta").get_text()
        fechaInicio = self.builder.get_object("selec_fe_ini_new_venta").get_text()
        fechaFin = self.builder.get_object("selec_fe_fin_new_venta").get_text()
        fechaVenta = time.strftime("%d-%m-%y")
        print("Datos a insertar de venta: ")
        print("Cliente ID: "+clienteID)
        print("Paquete ID: "+paqueteID)
        print("Fecha de inicio: "+fechaInicio)
        print("Fecha de fin: "+fechaFin)
        print("Fecha de venta: "+fechaVenta)

        ventanaError = self.builder.get_object("ventanaError")
        
        error=0
        print(error)
        
        #print(type(clienteID))
        
        if clienteID == "":
            print("Muestro error por CAMPO VACIO de venta CLIENTE")
            ventanaError.format_secondary_text("Tienes que seleccionar un cliente")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
        
        if paqueteID == "":
            print("Muestro error por CAMPO VACIO de venta PAQUETE")
            ventanaError.format_secondary_text("Tienes que seleccionar un paquete")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
            
        if fechaInicio == "Selecciona fecha..." or fechaInicio == "":
            print("Muestro error por CAMPO VACIO de venta FECHAS")
            ventanaError.format_secondary_text("Tienes que seleccionar una fecha de inicio y de fin")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
            
        if fechaFin == "Selecciona fecha..." or fechaFin== "":
            print("Muestro error por CAMPO VACIO de venta FECHAS")
            ventanaError.format_secondary_text("Tienes que seleccionar una fecha de inicio y de fin")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
        
        """Parseo a Integer los IDs
        clienteIdInt = int(clienteID);
        paqueteIdInt = int(paqueteID);"""
        
        if error==0:
            try:
                self.db.execute("INSERT INTO Venta (fechaVenta,fechaInicio,fechaFin,IdCli,IdPaq) VALUES (?,?,?,?,?)",(fechaVenta,fechaInicio,fechaFin,clienteID,paqueteID))
            except(sqlite3.ProgrammingError, ValueError, TypeError) as tipoError:
                ventanaError.format_secondary_text(tipoError)
                ventanaError.run()
                ventanaError.hide()
            else:
                print("Venta guardada correctamente :)")
                ventanaOk = self.builder.get_object("exitoAviso")
                ventanaOk.format_secondary_text("Venta guardada correctamente")
                ventanaOk.run()
                ventanaOk.hide()
                
                #Vuelvo a cargar la lista de clientes y oculto la de nueva venta
                self.lista_ventas("","liststore3","")
                self.builder.get_object('nuevaVenta').hide()
                self.builder.get_object('ventas').show()
        
    #Cancelo nueva venta
    def on_cancel_new_venta_clicked(self,widget):
        print("Cancelo nueva venta")
        vuelveVentas = self.builder.get_object("nuevaVenta")
        vuelveVentas.hide()
    
    #Modificar una venta BOTON DEL FORMULARIO
    def on_modificaVentaBtn_clicked(self,widget):
        clienteID = self.builder.get_object("idFormClienteVenta").get_text()
        paqueteID = self.builder.get_object("idFormPaquetesVenta").get_text()
        fechaInicio = self.builder.get_object("selec_fe_ini_new_venta").get_text()
        fechaFin = self.builder.get_object("selec_fe_fin_new_venta").get_text()
        fechaVenta = time.strftime("%d-%m-%y")
        idVenta = self.builder.get_object('idVentaForm').get_text()
        
        print("Datos a insertar de venta: ")
        print("Cliente ID: "+clienteID)
        print("Paquete ID: "+paqueteID)
        print("Fecha de inicio: "+fechaInicio)
        print("Fecha de fin: "+fechaFin)
        print("Fecha de venta: "+fechaVenta)
        print("ID de venta: "+idVenta)
        
        ventanaError = self.builder.get_object("ventanaError")
        
        error=0
        print(error)
        
        #print(type(clienteID))
        
        if clienteID == "Selecciona un cliente...":
            print("Muestro error por CAMPO VACIO de venta")
            ventanaError.format_secondary_text("Tienes que seleccionar un cliente")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
        
        if paqueteID == "Selecciona un paquete...":
            print("Muestro error por CAMPO VACIO de venta")
            ventanaError.format_secondary_text("Tienes que seleccionar un paquete")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
            
        if fechaInicio == "Selecciona fecha..." or fechaFin == "Selecciona fecha...":
            print("Muestro error por CAMPO VACIO de venta")
            ventanaError.format_secondary_text("Tienes que seleccionar una fecha de inicio y de fin")
            ventanaError.run()
            ventanaError.hide()
            error=1
            print(error)
        
        #CONSULTA UPDATE: 
        #print("valor de var error fuera de if -> "+error)
        # Si no se ha producido algun error entonces intento guardar registro en BD
        if error==0:
            try:
                self.db.execute("UPDATE Venta SET fechaVenta = ?, fechaInicio = ?, fechaFin = ?, IdCli = ?, IdPaq = ? WHERE ventaID ='"+idVenta+"'",(fechaVenta,fechaInicio,fechaFin,clienteID,paqueteID))
            except(sqlite3.ProgrammingError, ValueError, TypeError) as tipoError:
                ventanaError.format_secondary_text(tipoError)
                ventanaError.run()
                ventanaError.hide()
            else:
                print("venta modificado correctamente :)")
                ventanaOk = self.builder.get_object("exitoAviso")
                ventanaOk.format_secondary_text("Se han modificado los datos de la venta correctamente")
                ventanaOk.run()
                ventanaOk.hide()
                
                self.builder.get_object('button1_busqVent').set_sensitive(False)
                self.builder.get_object('button1_mod_vent').set_sensitive(False)
                self.builder.get_object('button1_del_vent').set_sensitive(False)
                self.builder.get_object('entry1_busqVent').set_text('')
                self.builder.get_object('comboboxVentas').set_active(-1)
                #Vuelvo a cargar la lista de clientes
                self.lista_ventas("","liststore3","")#listado de ventas principal
                self.builder.get_object('nuevaVenta').hide()
    
    #Controlo seleccion de venta en listado antes de modificar y borrar
    def on_treeview2Vent_row_activated(self,widget,tipo,treeview):
        print("Modificar venta seleccionada en listado")
        #Oculto id venta
        self.builder.get_object('idVentaForm').set_visible(False)
        self.builder.get_object('idFormClienteVenta').set_visible(False)
        self.builder.get_object('idFormPaquetesVenta').set_visible(False)
        seleccion = self.builder.get_object("treeview2Vent").get_selection()
        print(type(seleccion))
        #Ahora cojo modelo de liststore y ruta
        (modelo, pathlist) = seleccion.get_selected_rows()
        for path in pathlist:
            tree_iter = modelo.get_iter(path) #puntero a la fila
            idVenta = modelo.get_value(tree_iter,5)
            print(idVenta)
        #Muestro ventana de nuevo venta con los datos rellenos
        self.builder.get_object('nuevaVenta').show()
        #cambio el titulo de la ventana
        self.builder.get_object('label_nueva_venta').set_text('MODIFICAR VENTA')
        #Desactivo boton guardar un activo modificar
        self.builder.get_object('modificaVentaBtn').set_sensitive(True)
        self.builder.get_object('guarda_new_venta').set_sensitive(False)
        #realizo la busqueda de datos del paquete seleccionado
        buscaVenta = self.db.execute("SELECT * FROM Venta WHERE ventaID = '"+idVenta+"'")
        #Pongo los datos de venta en el formulario de modificacion
        for row in buscaVenta:
            print(row)
            idCliente = str(row[4])
            idPaquete = str(row[5])
            self.builder.get_object("idFormClienteVenta").set_text(str(row[4]))
            self.builder.get_object("idFormPaquetesVenta").set_text(str(row[5]))
            self.builder.get_object("selec_fe_ini_new_venta").set_text(str(row[2]))
            self.builder.get_object("selec_fe_fin_new_venta").set_text(str(row[3]))
            self.builder.get_object('idVentaForm').set_text(idVenta)
        #Busco nombre del cliente
        buscaNombre = self.db.execute("SELECT nombre,apellidos FROM Cliente WHERE clienteID = '"+idCliente+"'")
        for row in buscaNombre:
            print(row)
            nombre= row[0]
            apellidos = row[1]
            nombreCompleto = nombre+" "+apellidos
            print(nombreCompleto)
            self.builder.get_object("sel_cli_new_venta").set_text(nombreCompleto)
        #Busco nombre del paquete
        buscaPaquete = self.db.execute("SELECT nombre FROM Paquete WHERE paqueteID = '"+idPaquete+"'")
        for row in buscaPaquete:
            print(row)
            paquet = row[0]
            self.builder.get_object("sel_paq_new_venta").set_text(paquet)
    # Activo mod y borrar venta
    def on_treeview2Vent_cursor_changed(self,widget):
        print("Activo boton de MOD y DEL VENTA")
        self.builder.get_object('button1_mod_vent').set_sensitive(True)
        self.builder.get_object('button1_del_vent').set_sensitive(True)
        

    #Modificar una venta SELECCIONANDO DESDE LISTADO
    def on_button1_mod_vent_clicked(self,widget):
        print("Modificar venta seleccionada en listado")
        #Oculto id venta
        self.builder.get_object('idVentaForm').set_visible(False)
        self.builder.get_object('idFormClienteVenta').set_visible(False)
        self.builder.get_object('idFormPaquetesVenta').set_visible(False)
        seleccion = self.builder.get_object("treeview2Vent").get_selection()
        print(type(seleccion))
        #Ahora cojo modelo de liststore y ruta
        (modelo, pathlist) = seleccion.get_selected_rows()
        for path in pathlist:
            tree_iter = modelo.get_iter(path) #puntero a la fila
            idVenta = modelo.get_value(tree_iter,5)
            print(idVenta)
        #Muestro ventana de nuevo venta con los datos rellenos
        self.builder.get_object('nuevaVenta').show()
        #cambio el titulo de la ventana
        self.builder.get_object('label_nueva_venta').set_text('MODIFICAR VENTA')
        #Desactivo boton guardar un activo modificar
        self.builder.get_object('modificaVentaBtn').set_sensitive(True)
        self.builder.get_object('guarda_new_venta').set_sensitive(False)
        #realizo la busqueda de datos del paquete seleccionado
        buscaVenta = self.db.execute("SELECT * FROM Venta WHERE ventaID = '"+idVenta+"'")
        #Pongo los datos de venta en el formulario de modificacion
        for row in buscaVenta:
            print(row)
            idCliente = str(row[4])
            idPaquete = str(row[5])
            self.builder.get_object("idFormClienteVenta").set_text(str(row[4]))
            self.builder.get_object("idFormPaquetesVenta").set_text(str(row[5]))
            self.builder.get_object("selec_fe_ini_new_venta").set_text(str(row[2]))
            self.builder.get_object("selec_fe_fin_new_venta").set_text(str(row[3]))
            self.builder.get_object('idVentaForm').set_text(idVenta)
        #Busco nombre del cliente
        buscaNombre = self.db.execute("SELECT nombre,apellidos FROM Cliente WHERE clienteID = '"+idCliente+"'")
        for row in buscaNombre:
            print(row)
            nombre= row[0]
            apellidos = row[1]
            nombreCompleto = nombre+" "+apellidos
            print(nombreCompleto)
            self.builder.get_object("sel_cli_new_venta").set_text(nombreCompleto)
        #Busco nombre del paquete
        buscaPaquete = self.db.execute("SELECT nombre FROM Paquete WHERE paqueteID = '"+idPaquete+"'")
        for row in buscaPaquete:
            print(row)
            paquet = row[0]
            self.builder.get_object("sel_paq_new_venta").set_text(paquet)
    
    #Eliminar una venta del listado
    def on_button1_del_vent_clicked(self,widget):
        print("Elimino una venta seleccionada del listado")
        #Cojo el handler de la fila seleccionada
        seleccion = self.builder.get_object("treeview2Vent").get_selection()
        print(type(seleccion))
        #Ahora cojo modelo de liststore y ruta
        (modelo, pathlist) = seleccion.get_selected_rows()
        for path in pathlist:
            tree_iter = modelo.get_iter(path) #puntero a la fila
            idVenta = modelo.get_value(tree_iter,5)
            print(idVenta)
        
        #Muestro mensaje para confirmar borrado de cliente
        ventanaConfirmar = self.builder.get_object("confirmar")
        ventanaConfirmar.format_secondary_text("¿Desea borrar la venta seleccionado?")
        respuesta=ventanaConfirmar.run()
        #respuestaSerá -5 si le hemos dado a Aceptar, será -6 si Cancelar
        ventanaConfirmar.hide()

        if respuesta==-5:
            print("Entro a BORRAR VENTA")
            self.db.execute("DELETE FROM Venta where ventaID="+str(idVenta))
                
            #Llamo a la ventana de exito al borrar cliente
            ventanaOk = self.builder.get_object("exitoAviso")
            ventanaOk.format_secondary_text("Venta borrada correctamente")
            ventanaOk.run()
            ventanaOk.hide()
            
            self.builder.get_object('button1_busqVent').set_sensitive(False)
            self.builder.get_object('button1_mod_vent').set_sensitive(False)
            self.builder.get_object('button1_del_vent').set_sensitive(False)
            self.builder.get_object('entry1_busqVent').set_text('')
            self.builder.get_object('comboboxVentas').set_active(-1)
            #Actualizo todos los listore
            self.lista_ventas("","liststore3","")
    
    #Activar boton buscar
    def on_comboboxVentas_changed(self,widget):
        print('Activo boton buscar ventas')
        self.builder.get_object('button1_busqVent').set_sensitive(True)
    
    #Busqueda de una venta
    def on_button1_busqVent_clicked(self,widget):
        print("Hago una busqueda de una venta")
        comboSeleccionado = self.builder.get_object('comboboxVentas').get_active_text()
        textoBusqueda = self.builder.get_object('entry1_busqVent').get_text()
        print("Busca: "+textoBusqueda+" en campo "+comboSeleccionado)
        self.lista_ventas(comboSeleccionado,"liststore3",textoBusqueda)
        self.builder.get_object('button1_busqVent').set_sensitive(False)
        self.builder.get_object('button1_mod_vent').set_sensitive(False)
        self.builder.get_object('button1_del_vent').set_sensitive(False)
        self.builder.get_object('entry1_busqVent').set_text('')
        self.builder.get_object('comboboxVentas').set_active(-1)

    #funcion para inicializar el treeview de ventas <--- PASO 1 --->
    def inicializa_listado(self,treeview):
        """Inicializa los CellRenderer de un treeview pasado como parámetro. Esto siempre se hará igual para cada TreeView"""
        celda = gtk.CellRendererText()
        columnas=self.builder.get_object(treeview).get_columns()
        i=0
        for col_i in columnas:
            col_i.pack_start(celda)
            col_i.add_attribute(celda,"text", i)
            i=i+1
        print("exito inicializando treeview ventas")
    
    # funcion que lista datos de bd en treeview de clientes
    def lista_ventas(self,tipo,lista,filtro):
            """Lista ventas. Si tipo es "" lo listo todo, si no, lo hace por tipo """
            self.lista=self.builder.get_object(lista)
            self.lista.clear()#Limpia la lista
            busqueda = ""

            if tipo=="":
                print("Llego a buscar ventas en BD")
                #result=self.db.execute('SELECT * FROM Venta')
                busqueda = self.db.execute('SELECT ventaID ,fechaVenta, fechaInicio, fechaFin, C.nombre, P.nombre FROM Cliente C, Paquete P, Venta V WHERE V.IdCli = C.clienteID AND V.IdPaq = P.paqueteID')
            elif tipo == "Cliente":
                print("Busco venta por nombre del cliente")
                busqueda = self.db.execute("SELECT ventaID ,fechaVenta, fechaInicio, fechaFin, C.nombre, P.nombre FROM Cliente C, Paquete P, Venta V WHERE V.IdCli = C.clienteID AND V.IdPaq = P.paqueteID AND C.nombre LIKE '%"+filtro+"%'")
            elif tipo == "Viaje":
                print("Busco venta por nombre del paquete")
                busqueda = self.db.execute("SELECT ventaID ,fechaVenta, fechaInicio, fechaFin, C.nombre, P.nombre FROM Cliente C, Paquete P, Venta V WHERE V.IdCli = C.clienteID AND V.IdPaq = P.paqueteID AND P.nombre LIKE '%"+filtro+"%'")
            elif tipo == "Fecha de inicio":
                print("Busco venta por fecha de inicio")
                busqueda = self.db.execute("SELECT ventaID ,fechaVenta, fechaInicio, fechaFin, C.nombre, P.nombre FROM Cliente C, Paquete P, Venta V WHERE V.IdCli = C.clienteID AND V.IdPaq = P.paqueteID AND fechaInicio LIKE '%"+filtro+"%'")
            elif tipo == "Fecha de fin":
                print("Busco venta por fecha de fin")
                busqueda = self.db.execute("SELECT ventaID ,fechaVenta, fechaInicio, fechaFin, C.nombre, P.nombre FROM Cliente C, Paquete P, Venta V WHERE V.IdCli = C.clienteID AND V.IdPaq = P.paqueteID AND fechaFin LIKE '%"+filtro+"%'")
            
            for row in busqueda: 
                #Empieza por la [1] porque el ID es la [0]
                # self.lista.append([row[4],row[5],row[1],row[2],row[3]])
                self.lista.append([row[1],row[2],row[3],row[4],row[5],row[0]])
                print("Listo ventas en tabla")


    # Boton buscar en formulario de busquueda de cliente para la venta
    def on_btn_busq_cli_new_venta_clicked(self,widget):
        print("Pulso buscar cliente en buscador de cliente para venta")
        comboSeleccionado = self.builder.get_object('comboboxSelCliVenta').get_active_text()
        textoBusqueda = self.builder.get_object('term_busca_cli_new_venta').get_text()
        print("Busca: "+textoBusqueda+" en campo "+comboSeleccionado)
        self.lista_cliente_venta(comboSeleccionado,"tabla_bus_cli_new_venta",textoBusqueda)
    
    # lista buscar cliente para venta
    def lista_cliente_venta(self,tipo,lista,filtro):
        print("Listado de clientes en nueva venta")
        self.lista=self.builder.get_object(lista)
        self.lista.clear()#Limpia la lista
        busqueda = ""
        
        if tipo == "":
            print("No listo nada hasta que introduza un tipo y filtro CLI_VENTA_BUSCAR")
        else:
            print("Listo clientes para venta por tipo "+tipo+" y filtro por "+filtro)
            busqueda = self.db.execute("SELECT clienteID, nombre, apellidos, dni, pasaporte FROM Cliente WHERE " + tipo + " LIKE '%"+filtro+"%'")
        
        for row in busqueda:
            self.lista.append([row[1],row[2],row[3],row[4],row[0]])
    
    
                
    #Boton buscar en formulario de busqueda de paquete para venta
    def on_btn_busq_paq_new_venta1_clicked(self,widget):
        print("Pulso buscar paquete en nueva venta")
        comboSeleccionado = self.builder.get_object('comboboxSelPaqVenta1').get_active_text()
        textoBuscar = self.builder.get_object('term_busca_paq_new_venta1').get_text()
        print("Busca: "+textoBuscar+" en campo "+comboSeleccionado)
        self.lista_paquete_venta(comboSeleccionado,'tabla_bus_paq_new_venta',textoBuscar)
    
    #Lista buscar paquete en nueva venta
    def lista_paquete_venta(self,tipo,lista,filtro):
        print("Listado de paquetes en nueva venta")
        self.lista=self.builder.get_object(lista)
        self.lista.clear()#Limpia la lista
        busqueda = ""
        
        if tipo == "":
            print("No listo nada hasta que introduza un tipo y filtro PAQ_VENTA_BUSCAR")
        else:
            print("Listo paquetes para venta por tipo "+tipo+" y filtro por "+filtro)
            busqueda = self.db.execute("SELECT paqueteID, nombre, precio, destino FROM Paquete WHERE " + tipo + " LIKE '%"+filtro+"%'")
        
        for row in busqueda:
            self.lista.append([row[3],row[1],row[2],row[0]])
    
    #Controlo que se ha seleccionado un paquete al buscarlo para la venta
    def on_treeview2_cursor_changed(self,widget):
        print("Activo boton seleccionar paquete tras cogerlo del listado treeview")
        self.builder.get_object('save_busc_paq_new_venta1').set_sensitive(True)
    
    #Controlo que se ha seleccionado un cliente al buscarlo para la venta
    def on_treeview3_cursor_changed(self,widget):
        print("Activo boton seleccionar cliente tras cogerlo del listado treeview")
        self.builder.get_object('save_busc_cli_new_venta').set_sensitive(True)
    
    #menu emergente en listado (treeview)
    def on_treeview2Vent_button_press_event(self,treeview,evento):
        print("Evento press en la lista de ventas")
        pulsado = evento.button
        # si pulsa boton derecho
        if pulsado == 3:
            print("has pulsado con el boton derecho del raton")
            #creo menu
            self.menu = gtk.Menu()
            #creo boton modificar
            menu_modificar = gtk.ImageMenuItem(gtk.STOCK_EDIT)
            self.menu.append(menu_modificar)
            menu_modificar.connect("activate", self.on_button1_mod_vent_clicked)
            #creo boton borrar
            menu_borrar = gtk.ImageMenuItem(gtk.STOCK_DELETE)
            self.menu.append(menu_borrar)
            menu_borrar.connect("activate", self.on_button1_del_vent_clicked)
            #muestro
            self.menu.popup(None,None,None,evento.button,evento.time)
            menu_modificar.show()
            menu_borrar.show()