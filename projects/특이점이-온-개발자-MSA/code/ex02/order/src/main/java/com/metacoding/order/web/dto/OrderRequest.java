package com.metacoding.order.web.dto;

public record OrderRequest(
    int productId,
    int quantity,
    Long price,
    String address
) {}
