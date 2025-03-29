CREATE MIGRATION m13fznx6uykowo7bg5qzsk6dxwtqsct3sjmntwf2qt5brt5z5j45lq
    ONTO m1gtf3uvttelq2ei3sbndtw7vkaxw3rzzucge5tscg2lqnainbvd7q
{
  ALTER TYPE default::Reply {
      CREATE REQUIRED PROPERTY created_at: std::datetime {
          SET REQUIRED USING (<std::datetime>{});
      };
  };
};
