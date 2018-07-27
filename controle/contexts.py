from hyper_resource.contexts import FeatureResouceContext, FeatureCollectionResourceContext
class BusinessModelContext(FeatureResouceContext):
    pass
class BusinessModelCollectionContext(FeatureCollectionResourceContext):
    pass

class GastoContext(FeatureResouceContext):
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

class GastoCollectionContext(FeatureCollectionResourceContext):
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

class TipoGastoContext(FeatureResouceContext):
    pass
class TipoGastoCollectionContext(FeatureCollectionResourceContext):
    pass

class UsuarioContext(FeatureResouceContext):
    pass
class UsuarioCollectionContext(FeatureCollectionResourceContext):
    pass

