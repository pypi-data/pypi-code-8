from braintree.search import Search

class CustomerSearch:
      address_extended_address             = Search.TextNodeBuilder("address_extended_address")
      address_first_name                   = Search.TextNodeBuilder("address_first_name")
      address_last_name                    = Search.TextNodeBuilder("address_last_name")
      address_locality                     = Search.TextNodeBuilder("address_locality")
      address_postal_code                  = Search.TextNodeBuilder("address_postal_code")
      address_region                       = Search.TextNodeBuilder("address_region")
      address_street_address               = Search.TextNodeBuilder("address_street_address")
      address_country_name                 = Search.TextNodeBuilder("address_country_name")
      cardholder_name                      = Search.TextNodeBuilder("cardholder_name")
      company                              = Search.TextNodeBuilder("company")
      created_at                           = Search.RangeNodeBuilder("created_at")
      credit_card_expiration_date          = Search.EqualityNodeBuilder("credit_card_expiration_date")
      credit_card_number                   = Search.TextNodeBuilder("credit_card_number")
      email                                = Search.TextNodeBuilder("email")
      fax                                  = Search.TextNodeBuilder("fax")
      first_name                           = Search.TextNodeBuilder("first_name")
      id                                   = Search.TextNodeBuilder("id")
      ids                                  = Search.MultipleValueNodeBuilder("ids")
      last_name                            = Search.TextNodeBuilder("last_name")
      payment_method_token                 = Search.TextNodeBuilder("payment_method_token")
      payment_method_token_with_duplicates = Search.IsNodeBuilder("payment_method_token_with_duplicates")
      phone                                = Search.TextNodeBuilder("phone")
      website                              = Search.TextNodeBuilder("website")
      paypal_account_email                 = Search.TextNodeBuilder("paypal_account_email")
