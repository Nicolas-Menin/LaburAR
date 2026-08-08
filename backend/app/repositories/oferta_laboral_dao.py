from sqlalchemy.orm import Session
from backend.app.models.oferta_laboral import OfertaLaboral
from backend.app.models.empleador import Empleador


class OfertaLaboralDAO:

    def __init__(self,db: Session):
        self.db = db


    def crear_oferta_laboral(self,oferta_laboral: OfertaLaboral):
        """Metodo para crear oferta laboral"""

        self.db.add(oferta_laboral)
        self.db.commit()
        self.db.refresh(oferta_laboral)

        return oferta_laboral


    def actualizar_oferta(self, oferta_laboral: OfertaLaboral):
        """Metodo para actualizar los datos de la oferta laboral"""

        self.db.commit()
        self.db.refresh(oferta_laboral)

        return oferta_laboral


    def buscar_por_id(self,id_oferta_laboral: int):
        """Metodo para traer informacion de oferta laboral mediante id"""

        return self.db.query(OfertaLaboral).filter(
            OfertaLaboral.id == id_oferta_laboral
        ).first()

    def listar_ofertas_laborales(self,offset: int = 0, limit: int = 10):
        """Metodo para traer ofertas laboraless"""

        return (self.db.query(
            OfertaLaboral.id,
            OfertaLaboral.empleador_id,
            OfertaLaboral.titulo,
            Empleador.nombre_negocio,
            OfertaLaboral.ubicacion,
            OfertaLaboral.direccion,
            OfertaLaboral.descripcion
            ).join(Empleador,
                   OfertaLaboral.empleador_id == Empleador.id
            )
            .offset(offset)
            .limit(limit)
            .all()
        )

