CREATE MIGRATION m1xyg6pnl7stm27jnwpqvgbob4msqixnbrobkw5k4vt6onw42liqyq
    ONTO m1cu3i4xlifzmx4zpsyf3tyc73tfszupwhefovxgbjglofa73czrca
{
  ALTER TYPE default::Rant {
      CREATE LINK replies := (.<parent_rant[IS default::Reply]);
  };
};
