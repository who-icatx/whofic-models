package None;

import java.util.List;
import lombok.*;






/**
  Description of BaseIndexTerm
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class BaseIndexTerm extends LanguageTerm {

  private boolean isInclusion;
  private String indexType;

}