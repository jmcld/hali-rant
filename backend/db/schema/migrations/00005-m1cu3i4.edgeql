CREATE MIGRATION m1cu3i4xlifzmx4zpsyf3tyc73tfszupwhefovxgbjglofa73czrca
    ONTO m1ryyvxuknmgfaabnlgfjxfrzobtcf5227ksrw4is74ukplzrk2o6a
{
  CREATE ABSTRACT TYPE default::Moderatable {
      CREATE REQUIRED PROPERTY flagged_offensive: std::bool {
          SET default := false;
      };
      CREATE REQUIRED PROPERTY visible: std::bool {
          SET default := true;
      };
  };
  ALTER TYPE default::Rant EXTENDING default::Moderatable LAST;
  ALTER TYPE default::Reply EXTENDING default::Moderatable LAST;
};
