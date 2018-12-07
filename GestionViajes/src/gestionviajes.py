# -*- coding: utf-8 -*-

import sys, os
#importo las funciones para la base de datos (class -> Conector)
from BBDD import *
#importo las funciones de GestionClientes (class -> GestionTablaClientes)
from GestionClientes import *
#importo las funciones de GestionPaquetes (class -> GestionTablaPaquetes)
from GestionPaquetes import *
#importo las funciones de GestionVentas (class -> GestionTablaVentas)
from GestionVentas import *

try:
    import pygtk
    pygtk.require("2.0") 
except:
    print "Error GTK"  
    sys.exit(1)
try:
    import gtk
    import gtk.glade
except:
        print "Error GTK"  
	sys.exit(1)

class GestionViajesGUI:
	"""Ejemplo de llamada a Interfaz GLADE"""
        
        

	def __init__(self):
            
            #Creo un objeto para la BD
            #con el nombre de la base de datos
            self.con = Conector("viajes.db")
            #Intento obtener conexion a la base de datos
            self.db = self.con.dame_conexion()
            
            #Ahora se evita que si se borra el fichero .db pueda arrancar creando de nuevo la tabla
            #Se busca si existe la tabla, si no existe crea el esquema
            res=self.db.execute("SELECT * from sqlite_master")
            if not res.fetchall(): 
                print "BD vacia" 
                self.con.crear_esquema('') 
            
            # Activo foreign keys
            if self.db.execute("PRAGMA foreign_keys=ON"):
                print("Activo pragma de FOREIGN KEYS")
                
            print("BD conectada")
		
            self.builder = gtk.Builder()
            self.builder.add_from_file("main.glade") #Fichero GLADE
                
            #Llamo al constructor del gestor de una de las tablas
            #donde se van a definir todas las funciones que conectan las senales
            GC = GestionTablaClientes(self.db,self.builder, self.con)
            GP = GestionTablaPaquetes(self.db,self.builder, self.con)
            GV = GestionTablaVentas(self.db,self.builder, self.con)
                
            self.builder.connect_signals({ #Definicion de Senales de asociacion GLADE-PYGTK
            "delete-event" : self.on_destroy,
            "on_ayuda_activate" : self.on_ayuda_activate,
            "on_acercaDe_activate" : self.on_acercaDe_activate,
            # abrir y cerrar secciones app
            "on_aMainDesdeCli_clicked" : GC.on_aMainDesdeCli_clicked,
            "on_aMainDesdePaq_clicked" : GP.on_aMainDesdePaq_clicked,
            "on_aMainDesdeVenta_clicked" : GV.on_aMainDesdeVenta_clicked,
            "on_button_main_clientes_clicked" : self.on_button_main_clientes_clicked,
            "on_button_main_ventas_clicked" : self.on_button_main_ventas_clicked,
            "on_button_main_paquetes_clicked" : self.on_button_main_paquetes_clicked,
            "on_reiniciaBD_activate" : self.on_reiniciaBD_activate,
            "on_salirApp_activate" : self.on_salirApp_activate,
            #Señales para seccion GestionClientes
            "on_add_cli_clicked" : GC.on_add_cli_clicked,
            "on_cogeFechaNewCli_clicked" : GC.on_cogeFechaNewCli_clicked,
            "on_cogeNewFechaNacCli_clicked" : GC.on_cogeNewFechaNacCli_clicked,
            "on_CancelNewCli_clicked" : GC.on_CancelNewCli_clicked,
            "on_SaveNewCli_clicked" : GC.on_SaveNewCli_clicked,
            "on_mod_cli_clicked" : GC.on_mod_cli_clicked,
            "on_ModNewCli_clicked" : GC.on_ModNewCli_clicked,
            "on_comboboxClientes_changed" : GC.on_comboboxClientes_changed,
            "on_cli_busca_cli_clicked" : GC.on_cli_busca_cli_clicked,
            "on_del_cli_clicked" : GC.on_del_cli_clicked,
            "on_treeview1_row_activated" : GC.on_treeview1_row_activated,
            "on_treeview1_cursor_changed" : GC.on_treeview1_cursor_changed,
            "on_treeview1_button_press_event" : GC.on_treeview1_button_press_event,
            #Señales para seccion GestionPaquetes
            "on_button_add_paq_clicked" : GP.on_button_add_paq_clicked,
            "on_button4CancelNewCli1_clicked" : GP.on_button4CancelNewCli1_clicked,
            "on_button4SaveNewCli1_clicked" : GP.on_button4SaveNewCli1_clicked,
            "on_buttonModPaqForm_clicked" : GP.on_buttonModPaqForm_clicked,
            "on_treeview2Paq_row_activated" : GP.on_treeview2Paq_row_activated,
            "on_button_mod_paq_clicked" : GP.on_button_mod_paq_clicked,
            "on_comboboxPaquetes_changed" : GP.on_comboboxPaquetes_changed,
            "on_paq_busca_pa_clicked" : GP.on_paq_busca_pa_clicked,
            "on_button_del_paq_clicked" : GP.on_button_del_paq_clicked,
            "on_treeview2Paq_cursor_changed" : GP.on_treeview2Paq_cursor_changed,
            "on_treeview2Paq_button_press_event" : GP.on_treeview2Paq_button_press_event,
            #Señales para seccion Ventas
            "on_button1_add_vent_clicked" : GV.on_button1_add_vent_clicked,
            "on_busq_cli_new_venta_clicked" : GV.on_busq_cli_new_venta_clicked,
            "on_busq_paq_new_venta_clicked" : GV.on_busq_paq_new_venta_clicked,
            "on_guarda_new_venta_clicked" : GV.on_guarda_new_venta_clicked,
            "on_comboboxSelCliVenta_changed" : GV.on_comboboxSelCliVenta_changed,
            "on_btn_busq_cli_new_venta_clicked" : GV.on_btn_busq_cli_new_venta_clicked,
            "on_save_busc_cli_new_venta_clicked" : GV.on_save_busc_cli_new_venta_clicked,
            "on_cancel_busc_cli_new_venta_clicked" : GV.on_cancel_busc_cli_new_venta_clicked,
            "on_btn_busq_paq_new_venta1_clicked" : GV.on_btn_busq_paq_new_venta1_clicked,
            "on_save_busc_paq_new_venta1_clicked" : GV.on_save_busc_paq_new_venta1_clicked,
            "on_cancel_busc_paq_new_venta1_clicked" : GV.on_cancel_busc_paq_new_venta1_clicked,
            "on_modificaVentaBtn_clicked" : GV.on_modificaVentaBtn_clicked,
            "on_treeview2Vent_row_activated" : GV.on_treeview2Vent_row_activated,
            "on_treeview2Vent_cursor_changed" : GV.on_treeview2Vent_cursor_changed,
            "on_comboboxSelPaqVenta1_changed" : GV.on_comboboxSelPaqVenta1_changed,
            "on_treeview2_cursor_changed" : GV.on_treeview2_cursor_changed,
            "on_treeview3_cursor_changed" : GV.on_treeview3_cursor_changed,
            "on_treeview2Vent_button_press_event" : GV.on_treeview2Vent_button_press_event,
            "on_treeview3_row_activated" : GV.on_treeview3_row_activated,
            "on_treeview2_row_activated" : GV.on_treeview2_row_activated,
            #Señales de fechas en venta
            "on_abre_cal_ini_new_venta_clicked" : GV.on_abre_cal_ini_new_venta_clicked,
            "on_cogeFecha_clicked" : GV.on_cogeFecha_clicked,
            "on_abre_cal_fin_new_venta_clicked" : GV.on_abre_cal_fin_new_venta_clicked,
            "on_cogeFechaFinVenta_clicked" : GV.on_cogeFechaFinVenta_clicked,
            "on_cancel_new_venta_clicked" : GV.on_cancel_new_venta_clicked,
            "on_button1_mod_vent_clicked" : GV.on_button1_mod_vent_clicked,
            "on_button1_del_vent_clicked" : GV.on_button1_del_vent_clicked,
            "on_comboboxVentas_changed" : GV.on_comboboxVentas_changed,
            "on_button1_busqVent_clicked" : GV.on_button1_busqVent_clicked,
            #Señales de cerrado desde la cruz de la ventana
            "on_clientes_destroy" : GC.on_clientes_destroy,
            "on_nuevoCliente_destroy" : GC.on_nuevoCliente_destroy,
            "on_calNewCli_destroy" : GC.on_calNewCli_destroy,
            "on_paquetes_destroy" : GP.on_paquetes_destroy,
            "on_nuevoPaquete_destroy" : GP.on_nuevoPaquete_destroy,
            "on_ventas_destroy" : GV.on_ventas_destroy,
            "on_nuevaVenta_destroy" : GV.on_nuevaVenta_destroy,
            "on_buscaClienteVenta_destroy" : GV.on_buscaClienteVenta_destroy,
            "on_buscaPaqueteVenta_destroy" : GV.on_buscaPaqueteVenta_destroy,
            "on_calendario_destroy" : GV.on_calendario_destroy,
            "on_calendarioFinVenta_destroy" : GV.on_calendarioFinVenta_destroy
            })
            #Inicio la aplicacion (ventana main) 
            self.main=self.builder.get_object("main")
            self.main.show()
            
            #Conexión las señales de borrado
            self.builder.get_object('clientes').connect("delete-event", GC.on_clientes_destroy)
            self.builder.get_object('nuevoCliente').connect("delete-event", GC.on_nuevoCliente_destroy)
            self.builder.get_object('calNewCli').connect('delete-event', GC.on_calNewCli_destroy)
            self.builder.get_object('paquetes').connect("delete-event", GP.on_paquetes_destroy)
            self.builder.get_object('nuevoPaquete').connect("delete-event", GP.on_nuevoPaquete_destroy)
            self.builder.get_object('ventas').connect("delete-event", GV.on_ventas_destroy)
            self.builder.get_object('nuevaVenta').connect("delete-event", GV.on_nuevaVenta_destroy)
            self.builder.get_object('buscaClienteVenta').connect("delete-event", GV.on_buscaClienteVenta_destroy)
            self.builder.get_object('buscaPaqueteVenta').connect("delete-event", GV.on_buscaPaqueteVenta_destroy)
            self.builder.get_object('calendario').connect("delete-event", GV.on_calendario_destroy)
            self.builder.get_object('calendarioFinVenta').connect("delete-event", GV.on_calendarioFinVenta_destroy)

            #Inicializo los treeview
            GC.inicializa_listado('treeview1')
            GP.inicializa_listado('treeview2Paq')
            GV.inicializa_listado('treeview2Vent')
            #Treeview busqueda de clientes venta
            GV.inicializa_listado('treeview3')
            #Treeview busqueda de paquetes venta
            GV.inicializa_listado('treeview2')

            
            #Muestro listado de tablas en treeview desde bd
            GP.lista_paquetes("","liststore2","")#listado de paquete principal
            GC.lista_clientes("","liststore7","")#listado de clientes principal
            GV.lista_ventas("","liststore3","")#listado de ventas principal
            #Datos de BD en venta->cliente
            GV.lista_cliente_venta("","tabla_bus_cli_new_venta","")
            #Datos de BD en venta->paquete
            GV.lista_paquete_venta("","tabla_bus_paq_new_venta","")
        
        # Funciones para el MAIN (abrir gest. clientes, ventas y paquetes)
        def on_destroy(self, widget=None, *signals):
            print("Salgo desde principal con X")
            self.db.commit()
            self.db.close() 
            gtk.main_quit()
        # Abre menu gestion cliente
        def on_button_main_clientes_clicked(self,widget):
            print("A gestion de clientes")
            ventana=self.builder.get_object("clientes")
            ventana.show()
            self.builder.get_object('cli_busca_cli').set_sensitive(False)
            self.builder.get_object('mod_cli').set_sensitive(False)
            self.builder.get_object('del_cli').set_sensitive(False)
            self.builder.get_object('entry_busq_cli').set_text('')
            self.builder.get_object('comboboxClientes').set_active(-1)
            #Me declaro un objeto de gestion clientes para inicializar el listado vacio
            #cada vez que cargo la ventana de clientes
            GestCli = GestionTablaClientes(self.db,self.builder, self.con)
            GestCli.lista_clientes("","liststore7","")
        
        #abre menu gestion de ventas
        def on_button_main_ventas_clicked(self,widget):
            print("A gestion de ventas")
            ventana = self.builder.get_object("ventas")
            ventana.show()
            self.builder.get_object('button1_busqVent').set_sensitive(False)
            self.builder.get_object('button1_mod_vent').set_sensitive(False)
            self.builder.get_object('button1_del_vent').set_sensitive(False)
            self.builder.get_object('entry1_busqVent').set_text('')
            self.builder.get_object('comboboxVentas').set_active(-1)
            GestVentas = GestionTablaVentas(self.db,self.builder, self.con)
            GestVentas.lista_ventas("","liststore3","")
        
        #Abre menu gestion paquetes
        def on_button_main_paquetes_clicked(self,widget):
            print("A gestion de paquetes")
            ventana=self.builder.get_object("paquetes")
            ventana.show()
            self.builder.get_object('paq_busca_pa').set_sensitive(False)
            self.builder.get_object('button_mod_paq').set_sensitive(False)
            self.builder.get_object('button_del_paq').set_sensitive(False)
            self.builder.get_object('entry1_busqPaq').set_text('')
            self.builder.get_object('comboboxPaquetes').set_active(-1)
            GestPaq = GestionTablaPaquetes(self.db,self.builder, self.con)
            GestPaq.lista_paquetes("","liststore2","")
        
        #boton reiniciar bd
        def on_reiniciaBD_activate(self,widget):
            print("Reinicio la base de datos y vuelvo a cargar los listados")
            self.con.crear_esquema("reinicia")
            self.db.commit()
            reinicioVentana = self.builder.get_object('reinicioVentana');
            reinicioVentana.run()
            reinicioVentana.hide()
        
        #boton para salir app
        def on_salirApp_activate(self, widget=None, *data):
            print("Cierro la aplicacion")
            self.db.commit()
            self.db.close() 
            gtk.main_quit()
        
        #Ver manual de usuario de la aplicación
        def on_ayuda_activate(self,widget):
            print("Abro el PDF con la ayuda")
            manual="manual.pdf"
            if (sys.platform=="linux"): 
                subprocess.call(["xdg-open", manual])
            else: 
                os.startfile(manual)
        
        #Ver información sobre el programa
        def on_acercaDe_activate(self,widget):
            print("Muestro información ACERCA DE")
            acercaDe = self.builder.get_object("ventanaAcercaDe")
            acercaDe.run()
            acercaDe.hide()
	
if __name__ == "__main__":
    v = GestionViajesGUI() #Llama a la Clase
    gtk.main() #Ejecuta el programa

