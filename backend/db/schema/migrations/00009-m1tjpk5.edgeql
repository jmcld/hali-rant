CREATE MIGRATION m1tjpk54bokkmxc4kw6v2lzwwuwhsqg4776ut462h3ax5qjk7neu4q
    ONTO m13fznx6uykowo7bg5qzsk6dxwtqsct3sjmntwf2qt5brt5z5j45lq
{
  ALTER TYPE default::Rant {
      ALTER PROPERTY geom {
          RENAME TO geometry;
      };
  };
};
