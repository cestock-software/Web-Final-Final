create or replace procedure sp_listar_atenciones(atenciones out SYS_REFCURSOR)
is
begin
    open atenciones for select * from atencion_medica;
end;
/
create or replace procedure sp_listar_estados(estados out SYS_REFCURSOR)
is
begin
    open estados for select * from estado_reserva where id_estado_reserva = 10;
end;
/
create or replace procedure sp_listar_info_carnet(carnet out SYS_REFCURSOR, v_rut number)
is
begin
    open carnet for 
        select 
            cp.nro_ficha,
            p.rut_paciente,
            gs.tipo_grupo,
            pr.tipo_prevision,
            s.nombre_sector,
            c.nombre_cesfam
        from carnet_paciente cp
        join paciente p on p.rut_paciente = cp.rut_paciente
        join grupo_sanguineo gs on gs.id_grupo = cp.id_grupo
        join prevision pr on pr.id_prevision = cp.id_prevision
        join sector s on s.id_sector = cp.id_sector
        join cesfam c on c.id_cesfam = cp.id_cesfam
        where p.rut_paciente = v_rut;
end;
/
create or replace procedure sp_listar_info_paciente(paciente out SYS_REFCURSOR, v_rut nvarchar2)
is
begin
    open paciente for 
        select 
            p.direccion, 
            c.nombre_comuna, 
            p.email, 
            p.nro_celular, 
            p.email_tutor, 
            p.nro_tutor,
            e.tipo_estado
        from paciente p 
        join comuna c on p.id_comuna = c.id_comuna
        join estado e on p.id_estado = e.id_estado
        where p.rut_paciente = v_rut;
end;
/
create or replace procedure sp_listar_info_receta_medica(receta out SYS_REFCURSOR, v_atencion_id number)
is
begin
    open receta for 
        select 
            rm.id_receta_medica,
            m.nombre_medicamento,
            mr.cantidad_recetada,
            mr.frecuencia,
            mr.duracion
        from receta_medica rm
        join atencion_medica a on rm.id = a.id
        join medicamento_recetado mr on rm.id_receta_medica = mr.id_receta_medica
        join medicamento m on mr.id_medicamento = m.id_medicamento
        where a.id = v_atencion_id;
end;
/
create or replace procedure sp_listar_medicamentos(medicamentos out SYS_REFCURSOR)
is
begin
    open medicamentos for select id_medicamento, nombre_medicamento from medicamento where id_estado = 1 and total_disponible > 0;
end;
/
create or replace PROCEDURE SP_INSERTAR_RECETA(
    V_ID_ATENCION IN NUMBER,
    V_DURACION IN VARCHAR2,
    V_FRECUENCIA IN VARCHAR2,
    V_CANTIDAD_RECETADA IN NUMBER,
    V_ID_MEDICAMENTO IN NUMBER,
    V_ID_ESTADO IN NUMBER,
    V_SALIDA OUT  NUMBER) IS
NRO_ERROR VARCHAR2(255);
CODIGO_ERROR VARCHAR2(255);
FECHA_HORA_ERROR DATE := SYSDATE ;  
LUGAR_ERROR VARCHAR2(255);
BEGIN
    INSERT INTO RECETA_MEDICA VALUES
        (SEQ_RECETA_MEDICA.NEXTVAL,
        V_ID_ATENCION);

    INSERT INTO MEDICAMENTO_RECETADO VALUES 
        (SEQ_MED_RECETADO.NEXTVAL,
        V_DURACION,
        V_FRECUENCIA,
        V_CANTIDAD_RECETADA,
        V_ID_MEDICAMENTO,
        SEQ_RECETA_MEDICA.CURRVAL,
        V_ID_ESTADO);

    COMMIT;
    V_SALIDA:= 1;
EXCEPTION
    WHEN OTHERS THEN
        NRO_ERROR := SQLCODE;
        CODIGO_ERROR := SQLERRM;        
        LUGAR_ERROR:='SP_INSERTAR_RECETA';
        V_SALIDA:=0;

        INSERT INTO ERROR (ID_ERROR, NRO_ERROR, CODIGO_ERROR,FECHA_HORA_ERROR,LUGAR_ERROR)
            VALUES (SEQ_ERROR.NEXTVAL,NRO_ERROR, CODIGO_ERROR, FECHA_HORA_ERROR,LUGAR_ERROR);      
END SP_INSERTAR_RECETA;