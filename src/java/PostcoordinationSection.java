package None;

import java.util.List;
import lombok.*;






/**
  An entity that holds the Postcoordination information of a WHO-FIC entity 
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class PostcoordinationSection extends ContentModelEntity {

  private String whoficEntityIri;
  private List<PostcoordinationSpecification> postcoordinationSpecifications;

}