
/**
 * Write a description of class Interfaz here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */

import java.lang.*;
import javax.swing.JOptionPane;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import java.lang.Object;
import java.awt.GridLayout;

public class Interfaz extends JFrame
{
    private Object[] options = {"Indexar","Experimento 1","Salir"};

    /**
     * Constructor for objects of class Interfaz
     */
    public Interfaz()
    {}

    public int comenzar()
    {
        int opcion = JOptionPane.showOptionDialog(null, 
                "Que desea hacer?", 
                "Seleccione una opcion", 
                JOptionPane.YES_NO_OPTION,
                JOptionPane.INFORMATION_MESSAGE, 
                null, 
                options,
                "Indexar");
        if (opcion == JOptionPane.CLOSED_OPTION || opcion == 2)
        {
            System.exit(1); 
        }

        return opcion;
    }

    public boolean[] configuracion(){
        JCheckBox stemmingCheck = new JCheckBox("Stemming");
        JCheckBox simbolosCheck = new JCheckBox("Signos de puntuacion");
        JCheckBox stopCheck = new JCheckBox("Elimina stop words");
        Object[] params = {stemmingCheck, simbolosCheck,stopCheck, "Aceptar", "Cancelar"};
        /*setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
        setSize(300, 100);
        setLayout(new GridLayout());
        getContentPane().add(stemmingCheck);
        getContentPane().add(simbolosCheck);
        getContentPane().add(stopCheck);
        setVisible(true);*/
        int n = JOptionPane.showOptionDialog(null,null, "Seleccione las opciones de indexado",JOptionPane.YES_NO_OPTION,
                JOptionPane.INFORMATION_MESSAGE, 
                null,  params, "Opciones");
         if (n == JOptionPane.CLOSED_OPTION || n == 4)
        {
            System.exit(1); 
        }
        boolean []vals = {stemmingCheck.isSelected(), simbolosCheck.isSelected(), stopCheck.isSelected()}; //stemm = [0], simbolos = [1], sin stopWords = [2]
        return vals;
    }
}
