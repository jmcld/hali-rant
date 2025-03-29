CREATE MIGRATION m1gtf3uvttelq2ei3sbndtw7vkaxw3rzzucge5tscg2lqnainbvd7q
    ONTO m1xyg6pnl7stm27jnwpqvgbob4msqixnbrobkw5k4vt6onw42liqyq
{
  ALTER TYPE default::Reply {
      DROP PROPERTY title;
  };
};
