from hyper_resource.contexts import FeatureResourceContext, FeatureCollectionResourceContext, NonSpatialResourceContext, \
    AbstractCollectionResourceContext


class BusinessModelContext(FeatureResourceContext):
    pass
class BusinessModelCollectionContext(FeatureCollectionResourceContext):
    pass

class GastoContext(NonSpatialResourceContext):
    """
     def attributes_contextualized_dict(self):
        dic_context =  {
            "valor": {
                "@id": "http://schema.org/Float",
                "@type": "http://schema.org/Float"
            },
            "tipo_gasto": {
                "@id": "http://schema.org/Integer",
                "@type": "@id",
            },
            "usuario": {
                "@id": "http://schema.org/Person",
                "@type": "@id",

            },
            "detalhe": {
                "@id": "http://schema.org/Text",
                "@type": "http://schema.org/Text"

            },
            "id": {
                "@id": "http://schema.org/Integer",
                "@type": "http://schema.org/Integer"

            },
            "data": {
                "@id": "http://schema.org/Date",
                "@type": "http://schema.org/Date"

            }
        }

        return dic_context
    """

class GastoCollectionContext(AbstractCollectionResourceContext):
    """
    def attributes_contextualized_dict(self):

        dic_context =  {
            "valor": {
                "@id": "http://schema.org/Float",
                "@type": "http://schema.org/Float"
            },
            "tipo_gasto": {
                "@id": "http://schema.org/Integer",
                "@type": "@id",
            },
            "usuario": {
                "@id": "http://schema.org/Person",
                "@type": "@id",

            },
            "detalhe": {
                "@id": "http://schema.org/Text",
                "@type": "http://schema.org/Text"

            },
            "id": {
                "@id": "http://schema.org/Integer",
                "@type": "http://schema.org/Integer"

            },
            "data": {
                "@id": "http://schema.org/Date",
                "@type": "http://schema.org/Date"

            }
        },

        return dic_context
    """

class TipoGastoContext(NonSpatialResourceContext):
    pass
class TipoGastoCollectionContext(AbstractCollectionResourceContext):
    pass

class UsuarioContext(NonSpatialResourceContext):
    pass
class UsuarioCollectionContext(AbstractCollectionResourceContext):
    pass

